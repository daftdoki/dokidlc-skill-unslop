# 🚀 Announcing Relay 2.4.1: A Pivotal Step Forward

We're thrilled to announce that Relay 2.4.1 is now available — and it's not just a patch release, but a testament to our commitment to reliability. This release delves into the core of the sync engine, delivering a seamless, robust, and intuitive experience for our 12,400 active workspaces.

## What's New

- **Performance:** Performance is dramatically improved — sync is now 38% faster on large workspaces thanks to the new batched writer.
- **Security:** We've addressed CVE-2026-31877, a path traversal issue in the attachment handler (reported by Priya Natarajan on 2026-09-02).
- **Stability:** Additionally, the retry logic has been enhanced to handle transient failures gracefully, ensuring your data stays safe.

## Why It Matters

In today's evolving landscape of distributed teams, sync reliability is crucial. It's worth noting that this release leverages a fundamentally new approach to conflict resolution, showcasing the interplay between speed, safety, and simplicity.

As one of our customers put it: “Relay is not just a tool — it’s the backbone of how our team collaborates, and 2.4 was a game-changer.”

## Getting Started

In order to upgrade, run `relay upgrade` from any workspace, or download the build from https://relay.example.com/releases/2.4.1. The release ships on 2026-09-14 and requires Node 20 or later.

We hope this helps you build faster than ever! Let us know what you think — we'd love to hear your feedback. 🎉
