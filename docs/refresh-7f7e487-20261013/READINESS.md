# Candidate refresh readiness

Candidate `main` SHA: `7f7e487c47a87e871dfef53345e2b71288008bff`. Use a fresh exact source checkout, not local core or its diagnostics. Accepted old series stays immutable.

Plan: 31 scenario/config cells, 93 participant cells, **1,434 measured samples + 93 warmups = 1,527 observations**. This preserves mixed graphs 20/100/1,000, tiny graphs 100/1,000, no-op/leaf/fanout/full/shared/one-percent, 1/2/4 worker study, cache-disabled full, target-leaf/target-subgraph/multi-target.

Current pre-refresh suite HEAD: `b3db302064e2baef1a40ca5ad6f62639c6215fe9`; old measured suite `56384cace6821a1541e7773cf1d8ce7a4c688ed8`. Commit additive refresh changes and freeze that new suite SHA before collection.

Comparators retained: **Node 22.22.1, npm 9.2.0, Turbo 2.11.7, Nx 23.3.0**; checked-in exact package/lock files are the installation authority. Retaining these reasonable recent versions isolates the candidate refresh better than simultaneous comparator updates. Record host package versions and all relevant executable hashes. Disable Nx daemon/cloud and telemetry using the existing ENV policy. No remote cache.

## Separate refresh harness changes

`campaign-refresh.py` starts at the first cell. It applies only the previously accepted Nx `Cache: Skipped (--skip-nx-cache)` receipt handling, refuses an existing destination, and writes candidate/binary/suite/affinity identity. The original campaign and continuation scripts remain unchanged. Generated tasks, command policy, C timer, mutation/order/counts/output oracle are unchanged. `probe.py` adds `NIFT` as an executable override and `TASK_RUNNER_PROBE_OUTPUT` as receipt destination; old defaults are preserved.

The old continuation runner skips 27 cells and requires existing observations. **Do not invoke it for this new full campaign.** The old campaign rejects the valid disabled-cache receipt. Use the new refresh runner.

## Bootstrap / correctness / official execution

From the new isolated suite checkout on its dedicated host:

```sh
mkdir -p work/tools investigation
cp docs/tools-package.json work/tools/package.json
cp docs/tools-package-lock.json work/tools/package-lock.json
(cd work/tools && npm ci --no-audit --no-fund)
git clone https://github.com/nift-dev/nift.git work/nift-source
git -C work/nift-source checkout --detach 7f7e487c47a87e871dfef53345e2b71288008bff
test "$(git -C work/nift-source rev-parse HEAD)" = 7f7e487c47a87e871dfef53345e2b71288008bff
test -z "$(git -C work/nift-source status --porcelain)"
make -C work/nift-source -j4
export NIFT="$PWD/work/nift-source/nift"
export NIFT_SOURCE_SHA=7f7e487c47a87e871dfef53345e2b71288008bff
"$NIFT" --version
sha256sum "$NIFT"
cc -O2 scripts/measure.c -o work/measure
cc -O2 scripts/tiny-body.c -o work/tiny-body
TASK_RUNNER_PROBE_OUTPUT="$PWD/work/refresh-cert/initial-probe.json" python3 scripts/probe.py
# Freeze/record actual CPU IDs; all children inherit this CPU set.
taskset -c 0-3 python3 scripts/campaign-refresh.py --smoke --output /opt/results/task-runners-refresh-smoke
python3 scripts/audit.py /opt/results/task-runners-refresh-smoke
taskset -c 0-3 python3 scripts/campaign-refresh.py --output /opt/results/task-runners-20261013-candidate-7f7e487
python3 scripts/audit.py /opt/results/task-runners-20261013-candidate-7f7e487
```

Install `git python3 build-essential autoconf automake libtool pkg-config` as needed; pin Node/npm before `npm ci`. Record normal Make build flags/configuration rather than benchmarking a local binary. Smoke retains one warmup plus one sample per participant cell (186 observations), not official evidence. Exact events, task count/order, concurrency ceilings, reconstructed outputs, cache receipts and planned counts must all pass. Failure/recovery probe observations remain qualitative correctness evidence outside official samples.

## Capability refresh requires new probes

Do **not** treat historical `feature_probes.py`/`environment_probe.py` as the candidate capability audit. Those scripts assert old unavailable outputless-node/environment-declaration behavior. They also write old tracked investigation receipts. Current baseline graph still uses receipts, explicit file dependencies and configured workers. Preserve that comparison.

Independently inspect/document/certify outputless declarations, environment input contracts, ensure vs force targets, worker CLI overrides, graph/query/explain, recovery and result restoration if the frozen candidate exposes them. Add supported-feature probes as a labelled supplement. Native task cache restoration must be distinguished from incremental skipping. A legacy unsupported-form rejection does not demonstrate absence of a newer supported API.

No correctness claim is made yet: the candidate build and both fresh probe/full-smoke gates are pending. Keep historical practitioner opinions untouched and derive the new human+agent / agent-primary decision matrix from refreshed evidence.
