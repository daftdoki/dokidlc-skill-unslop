#!/bin/sh
# One headless run of one eval in one arm, for the skill-creator loop.
#   run.sh WORKSPACE ITERATION EVAL_ID ARM RUN_NUMBER
# ARM is with_skill (this plugin by --plugin-dir) or without_skill (no
# plugins, no settings, no CLAUDE.md). Both arms run claude -p with
# --setting-sources "" so nothing on the machine leaks into the baseline.
# Writes outputs/, result.json, transcript.md, timing.json and grading.json
# under WORKSPACE/iteration-N/eval-ID-NAME/ARM/run-N/. Then aggregate with
# skill-creator's scripts.aggregate_benchmark and open eval-viewer.
set -eu
E=$(cd "$(dirname "$0")" && pwd)
W=$1; iter=$2; id=$3; arm=$4; run=$5
SKILL_DIR=${SKILL_DIR:-$(cd "$E/../../.." && pwd)}
MODEL=${MODEL:-claude-opus-5}
name=$(python3 -c "import json,sys;print(next(e['name'] for e in json.load(open('$E/evals.json'))['evals'] if e['id']==$id))")
prompt=$(python3 -c "import json,sys;print(next(e['prompt'] for e in json.load(open('$E/evals.json'))['evals'] if e['id']==$id))")
outfile=$(python3 -c "import json,sys;print(next(e['output'] for e in json.load(open('$E/evals.json'))['evals'] if e['id']==$id))")
files=$(python3 -c "import json,sys;print(' '.join(next(e['files'] for e in json.load(open('$E/evals.json'))['evals'] if e['id']==$id)))")
evaldir="$W/iteration-$iter/eval-$id-$name"
rundir="$evaldir/$arm/run-$run"
work="$rundir/work"
rm -rf "$rundir"; mkdir -p "$work" "$rundir/outputs"
for f in $files; do cp "$E/inputs/$f" "$work/"; done
[ -f "$evaldir/eval_metadata.json" ] || python3 -c "import json;e=next(e for e in json.load(open('$E/evals.json'))['evals'] if e['id']==$id);json.dump({'eval_id':$id,'eval_name':e['name'],'prompt':e['prompt'],'assertions':e['assertions']},open('$evaldir/eval_metadata.json','w'),indent=2)"
case "$arm" in
  with_skill) extra="--plugin-dir $SKILL_DIR" ;;
  without_skill) extra="" ;;
  *) echo "arm must be with_skill or without_skill" >&2; exit 2 ;;
esac
cd "$work"
start=$(date +%s)
# shellcheck disable=SC2086
claude -p --setting-sources "" $extra --model "$MODEL" --permission-mode acceptEdits --allowedTools "Read,Write,Edit" \
  --output-format json "$prompt" > "$rundir/result.json" 2> "$rundir/stderr.log" || echo "claude exited $?" >> "$rundir/stderr.log"
end=$(date +%s)
[ -f "$work/$outfile" ] && cp "$work/$outfile" "$rundir/outputs/$outfile"
python3 - "$rundir" "$start" "$end" <<'PY'
import json, sys
rundir, start, end = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
try:
    r = json.load(open(f"{rundir}/result.json"))
except Exception:
    r = {}
u = r.get("usage", {})
tokens = sum(u.get(k, 0) for k in ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
ms = r.get("duration_ms", (end - start) * 1000)
json.dump({"total_tokens": tokens, "duration_ms": ms, "total_duration_seconds": round(ms / 1000, 1),
           "model": list(r.get("modelUsage", {}).keys()), "num_turns": r.get("num_turns"), "cost_usd": r.get("total_cost_usd")},
          open(f"{rundir}/timing.json", "w"), indent=2)
open(f"{rundir}/transcript.md", "w").write(r.get("result", "") or "")
PY
python3 "$E/tells.py" "$E/evals.json" "$id" "$rundir/outputs/$outfile" $( [ -n "$files" ] && echo "$E/inputs/${files%% *}" ) > "$rundir/grading.json"
python3 -c "import json;g=json.load(open('$rundir/grading.json'))['summary'];t=json.load(open('$rundir/timing.json'));print('$arm run-$run eval-$id: %d/%d in %ss, %s tokens' % (g['passed'],g['total'],t['total_duration_seconds'],t['total_tokens']))"
