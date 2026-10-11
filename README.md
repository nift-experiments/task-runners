# Task runners

A correctness-gated Nift Labs comparison of Nift 4.11.0, Turborepo 2.11.7 and Nx 23.3.0 as project task orchestrators. Accepted same-node campaign: **1,527 observations, 1,434 measured samples, 93 warmups and 93 runner cells**. Exact task sets, ordering, concurrency and outputs passed independent audit.

[Live report](https://lab.nift.dev/benchmarks/task-runners/) · [Canonical evidence](https://github.com/nift-experiments/lab-evidence/tree/main/benchmarks/task-runners/20261011-v4110) · [Results](docs/RESULTS.json) · [Methodology](docs/METHODOLOGY.md) · [Reproduction](docs/REPRODUCE.md) · [Practitioner review](docs/NIFT-TASK-RUNNER-DX-REVIEW.md)

Frozen Nift source `8f90fd49d8b2484c1d732cb440ea442e53e08172`; measured suite `56384cace6821a1541e7773cf1d8ce7a4c688ed8`. Node 22.22.1, npm 9.2.0. One fresh 4-shared-vCPU / 8-GB Ubuntu Linode. Mixed graphs: 20/100/1,000 tasks; tiny graphs: 100/1,000. No remote cache; Nx daemon disabled.

At 1,000 mixed tasks, median unchanged invocation: Nift 134.678 ms, Turbo 488.866 ms, Nx 2,089.225 ms. Full-dirty invocation: Nift 17.208 s, Turbo 148.163 s, Nx 26.513 s. These are controlled synthetic end-to-end observations including native launch layers, not universal JavaScript application or scheduler rankings. All samples retained; sparse expensive cells have only three measured samples. RSS is maximum-child high water, not summed process-tree memory.

The frozen harness’s final cache-disabled Nx receipt required a reporting-only continuation; rejected partial warmups are preserved separately. Commands, bodies and timing boundaries did not change. See reproduction for the precise correction.

42 separate remote semantic observations certify failure/recovery, environment and outputless boundaries, deleted-output behavior and post-target follow-up. Nift core was not modified. Useful explicit contracts are distinguished from redundant ceremony. Nift is compelling for bespoke authored workflows; Turbo/Nx retain native cache and ecosystem advantages. See [core handover](docs/CORE-HANDOVER.md).
