# Task-runners experiment handover

User scope: public `nift-experiments/task-runners`, fair same-node Nift/Turbo/Nx task-runner evaluation, canonical evidence in lab-evidence, dedicated Labs report and qualitative practitioner assessment. Commit/push checkpoints. Do not modify Nift core or historical campaigns.

Local feasibility first: equivalent underlying work, exact event/output/order/failure oracle, short timings and runtime budget before provisioning one cheap fresh Linode. Stop and report if comparable semantics cannot be expressed without hidden orchestration. Unsupported features must be labelled, not faked.

Inspect natural Nift direct `.f` task scripts separately from tracked artifact/DAG ownership. Check-only tasks cannot silently become clean merely because a synthetic success artifact exists. Environment invalidation cannot be claimed from runtime getenv alone. Cache hits restoring outputs are not ordinary incremental skipping.

No remote cache. Disable telemetry/cloud integrations and Nx daemon for controlled fresh CLI invocation measurements. Retain all observations and rejected attempts. Freeze tool versions, Nift source and suite commit before official measurement. No outlier removal. Failure scenarios are semantic tests, not successful timing samples.

Publish experiment/evidence first; Labs source stage then publication main as specified in this campaign brief; verify live before deleting cloud resource. Preserve distinct measured, publication and lifecycle identities. Verify CLI absence/API404, remove temporary keys/config/known-host material and scan published material for secrets. Use existing evidence layouts.
