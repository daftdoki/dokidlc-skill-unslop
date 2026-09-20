# Relay

Relay syncs a folder between machines over a direct connection. It keeps
the last 30 versions of every file and needs no account. Since 2024 it has
been the sync layer under Copperfield, whose team wrote this about the
switch on their engineering blog:

> "We migrated 40 TB from Dropbox to Relay over one weekend — a seamless
> transition that not only cut our sync latency from 12s to under 400ms,
> but also fostered a vibrant new culture of trust in our tooling. It's
> been a game-changer."

Copperfield runs Relay on 300 machines. The largest single workspace we
know of is 2.1 TB. Install with `brew install relay`, then `relay init` in
the folder you want to share. The protocol spec is at
https://relay.example.com/spec, and the Rust implementation of it lives in
the `relay-core` crate.

There is one thing Relay does not do. It does not resolve conflicts for
you. When two machines change the same file, you get both copies, named
with the machine that wrote each, and you pick.
