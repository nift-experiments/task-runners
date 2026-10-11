# Would I actually use Nift as a task runner?

Qualitative practitioner assessment, separate from the measured performance evidence.

**Yes, with caveats.** Nift is technically a programmable task runner: arbitrary actions, dependency ordering, bounded concurrency, declared file invalidation, targeted invocation and nonzero failure propagation are real supported behaviors. The tracked artifact model is not equivalent to Turbo/Nx's outputless target model, and `.f` scripting alone must not be credited as an incremental parallel scheduler.

## Natural authoring, rather than adapter line count

The measured Nift adapter uses one reusable `tasks/action.f`, not one large generated script per task. It reads the supported hook target/root environment and uses `cmd(...).cwd(...).run()`, rejecting unsuccessful launches/exits. Task identity, prerequisite order and output ownership reside in tracking; consumed file inputs reside in dependency sidecars. Turbo uses package scripts and task configuration; Nx uses run-commands targets, declared inputs and dependent output inputs. All three runners schedule work themselves.

Direct authored scripts are useful separately: a lint or test check can run without an output file, while package/release scripts can execute procedural policy over prepared prerequisites. Direct invocation does not automatically promise target closure, incremental state or bounded parallel execution. The experiment exercises these boundaries rather than introducing an adapter scheduler to conceal them.

## Explicitness can help agents

Artifact ownership, ordering, invalidation, lifecycle and action identity are different semantic facts. Nift's `depends` is completion order; file dependencies express staleness. Nx also has separate ordering and consumed-output declarations. An agent can inspect or rewrite these contracts without reverse-engineering shell commands, and independent tooling can check the execution/output graph.

More files or lines are not intrinsically a disadvantage. Redundant synchronized values and incomplete consumption relationships are the problem. A concise `consumes`-style authoring helper could derive the common ordering-plus-invalidation case while preserving explicit canonical contracts. This campaign does not establish that Nift already rejects every contradictory relationship before execution. It establishes the declared tested graphs and their behavior.

## Present-day preferences

- Bespoke procedural automation, especially agent-maintained: I would choose Nift when its supported process/file APIs cover the job. Reusable `.f` policy with explicit contracts is preferable to increasingly complicated package-script strings.
- Website, assets, native helpers and developer tasks in one Nift project: Nift is compelling as a single project/runtime model.
- Conventional package-script pipeline with reusable local/remote outputs: I would choose Turbo for its native caching and established JavaScript workflow integration. Remote caching was not benchmarked here.
- Large project graph relying on plugins, generators, framework integration and project tooling: I would choose Nx for that surrounding ecosystem. Its daemon-assisted default latency was not benchmarked.
- A few simple always-run recipes: Just is an attractive simpler choice. Just/mise were not quantitative participants and receive no speed ranking.

At equal measured performance I would retain the same ecosystem distinctions. I prefer Nift for bespoke procedural policy, not because every workload should be migrated. There is no inherent architectural need for a second executor when Nift supplies the required semantics, reliability and integration. A mature-Nift preference is conditional on the actual missing capabilities, not inferred from timing alone.

## Largest advantage and blocker

The strongest advantage is programmable `.f` policy plus inspectable artifact contracts. This materially improves the authoring experience over forcing all behavior into package command strings.

The biggest blocker is the divide between direct outputless tasks and tracked DAG outputs. Native environment inputs, ensure-versus-force targeting, per-invocation worker controls, graph explanation and smoother unfinished-build recovery would also help. Current `getenv` reads do not declare invalidation; normal retry after the injected failure requires `build --repair`. These are concrete semantics/ergonomics follow-ups. Nift core was not changed.

Defensible positioning: **Nift is a programmable task runner and tracked build system for authored workflows, with explicit artifact and dependency contracts.** Do not claim native cache, outputless DAG or JavaScript ecosystem feature parity.
