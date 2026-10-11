# Official same-node plan

Suite measurement revision: `56384cace6821a1541e7773cf1d8ce7a4c688ed8`.
Nift source: `8f90fd49d8b2484c1d732cb440ea442e53e08172`, reports v4.11.0.
Clean source archive SHA256: `f40e5650140494c1a26bb0a6fe87629ee1ab653d61b33439480693fda919e3ec`.
Pinned Turbo 2.11.7 / Nx 23.3.0 / Node 22.22.1 / npm 9.2.0.

One fresh g6-standard-4 Linode, 4 shared vCPU / 8 GB, Ubuntu 24.04, us-east. CLI type lookup returned USD 0.072/hour; cost depends on actual billed lifetime, not just timed work. Forecast 45–90 minutes of measurement, plus setup/publication. No second node or remote cache.

93 runner cells, 1,527 observations including 93 warmups. See frozen official-plan.json. Rotate runner order within each round. Cases interleave according to the frozen ordered plan; **scenario order is fixed, not rotated**, a limitation disclosed in the report. Setup and mutations precede the C timer, oracle follows it. No sample deletion. A rejected campaign is retained separately and never pooled with replacement measurements.

Before launch: exact source and participant versions, executable hashes, OS/kernel/CPU/RAM/filesystem inventory, CPU affinity, suite cleanliness and schema/semantic certification. Expected node and suite identities are recorded independently from later evidence/publication/lifecycle commits.

Evidence destination follows existing canonical convention: `lab-evidence/benchmarks/task-runners/20261011-v4110/`, with numeric/raw observations, traces, summary, environment/provenance, frozen protocol, audit, variance and lifecycle/publication receipts. Labs receives only compact summaries, pinned references and graphs.

Delete the node after publication/live verification. Independently verify CLI absence and API404, then remove temporary authorized SSH access/key, known-host state and CLI configuration. No credential or private connection state belongs in any repository.
