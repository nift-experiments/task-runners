# Measurement protocol — accepted scope

## Common execution contracts

Canonical task graph: stable task identity, explicit prerequisite list, declared input files, output files (possibly empty), deterministic body type and workload parameters. Independent oracle derives selected closure, dirty closure, event order, permitted failure continuations and expected output hashes. Every accepted observation requires no missing/duplicate/extra starts, matching completions and hashes, prerequisite completion before consumer start, bounded peak concurrency and nonzero failure exits.

Separate artifact tasks and outputless checks. Task bodies are identical processes across runners; adapters declare policy only. The small graph models generation/check/build/package/release roles with controlled JSON records, property assertions, text transforms, one trivial real C helper compilation/execution and in-memory archive validation. Task names do not denote real TypeScript/framework/application test tools. Generated families test 20/100/1,000 tasks and 100/1,000 tiny tasks; optional 10,000 excluded after feasibility.

## Cohorts

1. Cache-disabled local execution: explicitly execute selected closure, common worker bounds; no synthetic skip layer.
2. Incremental unchanged/changed-input behavior: retained successful state; distinguish Nift tracked clean checks from Turbo/Nx local cache replay. Compare required underlying work only after semantic certification; do not assert the mechanisms are identical.
3. Output restoration: separate local cache feature study; Nift rebuilding missing outputs is not a cache hit.
4. Always-run/outputless checks: independent semantic track; do not hide checks behind markers.
5. Direct authored Nift scripts: qualitative/semantic assessment, not assumed equivalent to tracked parallel scheduling.

## Matrix and gates

Warm unchanged, leaf dirty, shared input dirty, medium fan-out, full dirty, targeted leaf/closure/multiple targets, workers 1/2/4, failure/blocking/recovery, file/generated input changes, environment inputs where supported, mixed bodies and tiny 1%/10% dirty scaling. Cache-disabled all-run and forced-target cases are distinct from ensure-target cases. Unsupported concepts receive bounded exclusions, not invented parity.

Retain subprocess start/completion/failure traces using a common logger, deterministic output hashes, per-run runner stdout/stderr and parsed selection/cache diagnostics. Blocked versus clean/cache-skipped labels require runner evidence plus independent closure checks; absence from a trace alone is insufficient to infer why a task did not run.

Linux C supervisor: wall time and wait4 child CPU/max-child RSS; RSS is not aggregate simultaneous process-tree memory. Setup/mutation/oracle outside timer. Stdout/stderr captured; native status/cache-log formatting costs are included, terminal painting excluded. Turbo uses errors-only task logs; Nx uses static output, with each invocation retained. These are CLI/orchestration measurements, not isolated scheduler CPU. Same node/compiler/files/workers, rotated runner order; fixed scenario order, explicit daemon/cache state. No cold-machine claim. Frozen workload-sensitive counts: 50 unchanged, 20 one-leaf changes, 10 small work, 5 moderate work and 3 expensive large work. One retained warmup per runner/cell. See official-plan.json for the exact 31 scenario/config cells (93 runner cells). Keep every sample.

Before cloud: freeze supported versions and Nift executable source/build identity, certify all adapters, identify scope exclusions and estimate wall/cost budget. Official campaign must pass independent audit, variance review and private-material scan before publication. Slow Nift paths produce a diagnostic handover; core changes are out of scope.

Input mechanism distinction: Nift declares prerequisite artifact files; Nx uses dependentTasksOutputFiles; Turbo propagates native prerequisite task hashes through dependsOn. The common changed-input cases verify their required work sets, not equivalence under arbitrary manual edits to cached output files.

Failure injection forces task execution so cached success cannot conceal the failure. Recovery certifies full forced execution for Turbo/Nx and build --repair for Nift; fastest default incremental retry latency is not a measured claim.
