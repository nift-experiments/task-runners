# Protocol draft — no measurements yet

## Common execution contracts

Canonical task graph: stable task identity, explicit prerequisite list, declared input files, output files (possibly empty), deterministic body type and workload parameters. Independent oracle derives selected closure, dirty closure, event order, permitted failure continuations and expected output hashes. Every accepted observation requires no missing/duplicate/extra starts, matching completions and hashes, prerequisite completion before consumer start, bounded peak concurrency and nonzero failure exits.

Separate artifact tasks and outputless checks. Task bodies are identical processes across runners; adapters declare policy only. Realistic small graph combines JSON schema/client generation, lint/typecheck/unit checks, web text transformation, one helper compilation, deterministic archive packaging, integration checks, verification and release manifest. Generated families test 20/100/1,000 tasks and 100/1,000/10,000 tiny tasks if feasible.

## Cohorts

1. Cache-disabled local execution: explicitly execute selected closure, common worker bounds; no synthetic skip layer.
2. Incremental unchanged/changed-input behavior: retained successful state; distinguish Nift tracked clean checks from Turbo/Nx local cache replay. Compare required underlying work only after semantic certification; do not assert the mechanisms are identical.
3. Output restoration: separate local cache feature study; Nift rebuilding missing outputs is not a cache hit.
4. Always-run/outputless checks: independent semantic track; do not hide checks behind markers.
5. Direct authored Nift scripts: qualitative/semantic assessment, not assumed equivalent to tracked parallel scheduling.

## Matrix and gates

Warm unchanged, leaf dirty, shared input dirty, medium fan-out, full dirty, targeted leaf/closure/multiple targets, workers 1/2/4, failure/blocking/recovery, file/generated input changes, environment inputs where supported, mixed bodies and tiny 1%/10% dirty scaling. Cache-disabled all-run and forced-target cases are distinct from ensure-target cases. Unsupported concepts receive bounded exclusions, not invented parity.

Retain subprocess start/completion/failure traces using a common logger, deterministic output hashes, per-run runner stdout/stderr and parsed selection/cache diagnostics. Blocked versus clean/cache-skipped labels require runner evidence plus independent closure checks; absence from a trace alone is insufficient to infer why a task did not run.

Linux C supervisor: wall time and wait4 child CPU/max-child RSS; RSS is not aggregate simultaneous process-tree memory. Setup/mutation/oracle outside timer. Same node/compiler/files/workers, rotated runner and scenario order, explicit daemon/cache state. No cold-machine claim. Workload-sensitive sample counts: 100 no-op/tiny, 20 moderate, 5 multi-second, 3 expensive; final bounded plan after feasibility. Keep every sample.

Before cloud: freeze supported versions and Nift executable source/build identity, certify all adapters, identify scope exclusions and estimate wall/cost budget. Official campaign must pass independent audit, variance review and private-material scan before publication. Slow Nift paths produce a diagnostic handover; core changes are out of scope.
