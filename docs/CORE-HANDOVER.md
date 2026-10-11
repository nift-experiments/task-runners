# Task-runner semantic follow-up — no core edits

This is a bounded capability/ergonomics handover, not a claim of a measured performance defect. Frozen Nift source `8f90fd49d8b2484c1d732cb440ea442e53e08172`; measured suite `56384cace6821a1541e7773cf1d8ce7a4c688ed8`.

## Outputless checks in a native tracked DAG

Reproducer: `python3 scripts/feature_probes.py` generates the same mixed workflow with `checks='outputless'`. Turbo/Nx natively run outputless check targets with cache disabled. The Nift custom tracked hook reports `custom build did not produce the tracked output file` and blocks consumers. Direct `.f` lint succeeds.

Question for core: can explicit task nodes without artifact ownership participate in completion ordering and bounded parallel scheduling, with an independently declared always-run/cacheable policy? Preserve tracked artifact contracts; do not make a missing required output silently acceptable. Success receipts are a useful explicit cache policy, but are not native outputless parity.

## Environment invalidation

Reproducer: `python3 scripts/environment_probe.py` runs A then B. An action reads TASK_PROBE. Turbo `env` and Nx env inputs invalidate the target; Nift runtime getenv alone leaves it clean with the previous output.

Consider a declarative environment-input contract or a documented opt-in helper. A user-authored environment-to-file projection is possible policy, but should not be advertised as already-native automatic environment invalidation.

## Ordering and consumption

Current `depends` completion order and sidecar file-input staleness are different meaningful semantics. An authoring helper for consumes-output relationships could derive both contracts and validate missing ownership, while preserving the rich canonical representation. Evaluate contradictory definitions and graph introspection rather than merely minimizing line count.

## Targeting, workers and recovery

`probe.py` certifies a named Nift target is forced. A clean ensure-target mode would better express task-runner intentions without relying on deliberately dirty benchmark targets. The current adapter sets build-threads in project configuration; per-invocation worker override would improve ergonomics.

Injected schema failure permits independent branches and blocks descendants. Normal retry reports unfinished build; `build --repair` succeeds. Explain the unfinished lifecycle and affected/blocked set clearly; do not solve this by deleting metadata.

No Nift source or build-engine optimization was made in this experiment. Any timing diagnostic, if warranted by accepted same-node results, must remain separate from timing samples.
