# Task runners

A correctness-gated Nift Labs experiment comparing Nift, Turborepo and Nx as project task orchestrators. This repository contains the protocol and implementation; accepted raw evidence will live in `nift-experiments/lab-evidence`. No results exist yet.

The question is dependency orchestration, invalidation, concurrency, targeting and failure recovery, not merely process-launch latency. Identical deterministic task bodies and an independent graph/output oracle are required. Cache-disabled execution, unchanged-input skipping and cache restoration are distinct cohorts.

See [methodology](docs/METHODOLOGY.md), [participants](docs/PARTICIPANTS.md) and [handover](HANDOVER.md). No Nift core changes are authorized. Official measurement and Labs publication follow local semantic certification.
