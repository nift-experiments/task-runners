# Reproduce the frozen protocol

Use an isolated Linux measurement host, Node 22.22.1 and npm 9.2.0. The accepted environment inventory records the exact OS, kernel, Python/compiler versions, CPU set and executable hashes. Matching protocol does not guarantee identical shared-host timings.

Required system tooling: Git, Python 3, cc/C++ compiler, make, autoconf, automake, libtool and pkg-config (Ubuntu build-essential packages). Plotting and website dependencies are not measurement dependencies.

From a clone of this experiment, preserve any local edits and select frozen suite `56384cace6821a1541e7773cf1d8ce7a4c688ed8`. The following commands assume a clean isolated checkout:

```sh
mkdir -p work/tools work/nift-source
cp docs/tools-package.json work/tools/package.json
cp docs/tools-package-lock.json work/tools/package-lock.json
(cd work/tools && npm ci --no-audit --no-fund)
git clone https://github.com/nift-dev/nift.git work/nift-git
git -C work/nift-git archive 8f90fd49d8b2484c1d732cb440ea442e53e08172 > work/nift-source.tar
tar -xf work/nift-source.tar -C work/nift-source
make -C work/nift-source -j4
cc -O2 scripts/measure.c -o work/measure
cc -O2 scripts/tiny-body.c -o work/tiny-body
python3 scripts/probe.py
python3 scripts/feature_probes.py
python3 scripts/environment_probe.py
python3 scripts/campaign.py --output /absolute/new/results-directory
python3 scripts/audit.py /absolute/new/results-directory
```

Do not run the campaign over an existing observation directory: create a new empty destination. Participant order rotates within rounds; scenario order is fixed. The frozen plan has 31 scenario/config cells, 93 runner cells and 1,527 observations including 93 warmups. Every planned cell must be present for audit acceptance. The harness writes and verifies fixtures outside the C timer. No remote caching; Nx daemon disabled. Task bodies and native launch layers are retained unchanged.

Raw stdout/stderr, C metrics and task traces are originally flat beside observations. Canonical lab-evidence organizes them into action-logs/, metrics/ and action-traces/. For an independent canonical audit, copy observations/plan and stage those three directories' files flat in an external temporary directory before invoking the frozen auditor. Current explanatory methodology/scope outside protocol/ must not be mistaken for changes to the frozen measured source.

Publication renderer is in Labs and runs only after complete independent audit. It checks all raw median/sample counts before generating charts and exact tables. Warmups, semantic diagnostics and rejected local pilots never enter measured distributions.

## Cache-disabled receipt correction

The frozen harness stopped at the first Nx cache-disabled warmup: Nx 23.3.0 reports `Cache: Skipped (--skip-nx-cache)` instead of a numeric hit count. Its tasks and output oracle passed; the reporting assertion rejected that receipt. The first 27 complete cells (1,395 rows) remain unchanged. The two preceding warmups and failed Nx receipt are preserved separately and excluded. The final four cells restart with `scripts/campaign-continuation.py`, which recognizes this explicit disabled-cache receipt as zero hits, loads retained rows and continues global participant rotation. Commands, task bodies, timer, fixtures and sample counts are unchanged. This supplementary harness is recorded separately from the frozen suite.

For reproduction from scratch, apply the continuation script's cache-receipt branch to the frozen harness before running the full plan. For the exact resumed path, retain the first 1,395 rows, preserve rejected files separately, and execute the published continuation script from the same checkout. Then run the unchanged frozen auditor on the complete matrix.
