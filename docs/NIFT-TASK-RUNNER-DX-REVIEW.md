# Would I actually use Nift as a task runner?

Qualitative practitioner assessment, separate from the measured performance evidence.

**Yes, with caveats.** Nift is technically a programmable task runner: arbitrary actions, dependency ordering, bounded concurrency, declared file invalidation, targeted invocation and nonzero failure propagation are real supported behaviors. The tracked artifact model is not equivalent to Turbo/Nx's outputless target model, and `.f` scripting alone must not be credited as an incremental parallel scheduler.

## Natural authoring, rather than adapter line count

The measured Nift adapter uses one reusable `tasks/action.f`, not one large generated script per task. It reads the supported hook target/root environment and uses `cmd(...).cwd(...).run()`, rejecting unsuccessful launches/exits. Task identity, prerequisite order and output ownership reside in tracking; consumed file inputs reside in dependency sidecars. Turbo uses package scripts and task configuration; Nx uses run-commands targets, declared inputs and dependent output inputs. All three runners schedule work themselves.

Direct authored scripts are useful separately: a lint or test check can run without an output file, while package/release scripts can execute procedural policy over prepared prerequisites. Direct invocation does not automatically promise target closure, incremental state or bounded parallel execution. The experiment exercises these boundaries rather than introducing an adapter scheduler to conceal them.

## Explicitness can help agents

Artifact ownership, ordering, invalidation, lifecycle and action identity are different semantic facts. Nift's `depends` is completion order; file dependencies express staleness. Nx also has separate ordering and consumed-output declarations. An agent can inspect or rewrite these contracts without reverse-engineering shell commands, and independent tooling can check the execution/output graph.

More files or lines are not intrinsically a disadvantage. Redundant synchronized values and incomplete consumption relationships are the problem. A concise `consumes`-style authoring helper could derive the common ordering-plus-invalidation case while preserving explicit canonical contracts. This campaign does not establish that Nift already rejects every contradictory relationship before execution. It establishes the declared tested graphs and their behavior.

## Present-day choice, including equal performance

Equal performance would not make Turbo or Nx my default for authored workflows. I already prefer Nift for bespoke procedural and agent-maintained workflows when its current APIs cover the required behavior. This is a clarification of my judgement, not a new benchmark conclusion.

| Workflow | My choice at equal performance | Reason |
| --- | --- | --- |
| Bespoke authored workflow | Nift | Reusable `.f` procedural policy and explicit action/artifact relationships fit the work. |
| Agent-maintained workflow | Nift | Independently inspectable ownership, ordering, invalidation and lifecycle contracts make changes easier to verify. |
| Mixed website/assets/native/tools project | Nift | One project/runtime model is compelling when these tasks belong together. |
| JS monorepo requiring local/remote artifact reuse | Turbo | Native task-result restoration and shared caching, with package/workspace pipelines, satisfy requirements this Nift snapshot does not provide. |
| Large framework-heavy monorepo relying on Nx plugins/generators/affected tooling | Nx | That existing development platform avoids recreating project inference, framework configuration and maintenance tooling. |

These choices assume equivalent reliability and the needed APIs, not just equal stopwatch readings. I would not migrate a healthy established repository merely because another runner won this synthetic benchmark. A few simple always-run recipes may still favor Just; it was not quantitatively benchmarked.

## What would make me choose Turbo?

**Decision-changing task-runner capabilities:** a content-addressed task-result cache that restores declared output files/logs, and a remote/shared cache that reuses those results across developers and CI. Nift checking that retained outputs are clean is a different contract: it does not restore a missing artifact from a previous computation. These capabilities matter when repeated expensive deterministic tasks, clean checkouts or multiple machines make reuse valuable. Remote caching was not measured. [Turbo caching](https://turborepo.dev/docs/crafting-your-repository/caching), [remote caching](https://turborepo.dev/docs/core-concepts/remote-caching).

**Project integration:** package/workspace dependency discovery and package-script pipelines matter when the repository is already organized around those conventions. Filtering and persistent/dev-task conventions are conveniences for most bespoke workflows; they become requirements if everyday development needs package-aware selection or coordinated long-running tasks. They are not reasons for my general preference over Nift's authored policy. Persistent services were not tested here. [Workspace structure](https://turborepo.dev/docs/crafting-your-repository/structuring-a-repository), [run/filtering](https://turborepo.dev/docs/reference/run), [development tasks](https://turborepo.dev/docs/crafting-your-repository/developing-applications).

## What would make me choose Nx?

**Task-runner and selection capabilities:** hashed local/remote computation caching and output restoration; project-graph knowledge and affected-task selection that identify work from repository changes. A project graph and affected computation are more than basic prerequisite scheduling. This experiment's authored single-project graph does not establish parity with them. [Caching](https://nx.dev/docs/concepts/how-caching-works), [affected tasks](https://nx.dev/docs/features/ci-features/affected).

**Development-platform integration:** plugins can infer tasks and inputs/outputs, contribute project relationships, and provide generators, migrations and executors. Framework/tool integrations can therefore save substantial setup and upgrade work. I would choose Nx when those specific integrations are already valuable to the project, not because plugins intrinsically improve the underlying executor. IDE/dev tooling is normally convenience rather than a decisive requirement. [Nx plugin model](https://nx.dev/docs/concepts/nx-plugins).

**CI platform:** Nx Cloud distributed execution is a distinct multi-machine requirement, not the local worker scheduling tested here. It can decide a platform choice when distributed CI is actually needed; remote sharing/distributed execution were excluded from this campaign. Nx Cloud is not implied by merely choosing the local Nx CLI. [Nx Agents](https://nx.dev/docs/features/ci-features/distribute-task-execution).

## Rank the concrete Nift gaps

This is a preference-impact ranking for my authored-workflow use, not a universal priority list. Cache-heavy multi-machine projects move items 3 and 4 to the top.

1. **Native outputless tracked task nodes — task-runner semantics.** Lint/test checks should participate in a scheduled dependency graph without owning a synthetic artifact. Direct `.f` checks work, but do not supply that DAG contract.
2. **Declarative environment invalidation — task-runner correctness.** A runtime environment read alone does not declare staleness; an untracked environment change can leave an output clean. Explicit file projections can be authored, but are not native parity.
3. **Local task-result restoration — task-runner capability.** Valuable for missing outputs and repeated computations; distinct from retained-state incremental skipping.
4. **Optional shared remote caching — cross-machine capability.** Decisive where developer/CI reuse is required; not necessary for every authored workflow.
5. **Ensure-versus-force targeting — task-runner semantics/ergonomics.** Clean target selection should avoid needless execution while retaining an explicit force operation.
6. **Smoother failed-run recovery — lifecycle ergonomics.** The tested recovery uses `build --repair`; clearer retry and blocked-task explanations would reduce operational friction.
7. **Per-invocation workers and graph/query/explain — inspection/control ergonomics.** Useful for safe agent edits and diagnosing selection. These improve practical use without proving an architectural defect.

Nift need not reproduce the entire Nx platform to be a strong task runner. Native outputless behavior and environment inputs affect a broad correctness contract; generators, IDE integration and framework-specific migrations affect particular projects.

## Mature-Nift counterfactual

If Nift added reliable native outputless nodes, declarative environment inputs, local task-result restoration, optional shared remote caching, clean ensure-target semantics, per-invocation worker control, graph/query/explain tooling and smoother failure recovery while retaining `.f` programmability and explicit contracts, **I would not prefer Turbo or Nx as the default for a new authored task workflow**. I would choose Nift for bespoke, agent-maintained and mixed Nift projects.

I could still choose Turbo for a project whose package/workspace and persistent-development conventions make it a better fit, or retain Nx where project/affected inference, framework plugins, generators/migrations or distributed CI are essential. The proposed Nift additions do not automatically provide those integrations or distributed execution. Existing investment and migration cost can also justify retaining a working tool. Those are concrete capability/integration reasons, not an inherent architectural need for a second task executor. The counterfactual assumes these additions are reliable and fit for use; a feature checklist alone would not establish that.

## Performance and authoring both count

The accepted 1,000-task mixed / j4 observations favor Nift strongly: unchanged medians 134.678 / 488.866 / 2,089.225 ms, one-leaf medians 203.318 / 879.019 / 2,337.511 ms and full-dirty medians 17.208 / 148.163 / 26.513 s (Nift / Turbo / Nx). Full-build maximum-child RSS is 20.0 / 115.6 / 169.5 MiB. These remain synthetic end-to-end measurements, full-dirty cells have only three measured samples, RSS is not summed tree memory, and remote cache/Nx daemon-assisted defaults were not measured.

The result does not make Nift a universal replacement, but my preference is not merely a reward for its timing: its programmable policy and explicit contracts are independently attractive for the workflows I would already choose it for. Task running is a natural fit for the tested architecture. No measurements, methodology or canonical evidence changed in this qualitative refinement.

## Largest advantage and blocker

The strongest advantage is programmable `.f` policy plus inspectable artifact contracts. This materially improves the authoring experience over forcing all behavior into package command strings.

The biggest blocker is the divide between direct outputless tasks and tracked DAG outputs. Native environment inputs, ensure-versus-force targeting, per-invocation worker controls, graph explanation and smoother unfinished-build recovery would also help. Current `getenv` reads do not declare invalidation; normal retry after the injected failure requires `build --repair`. These are concrete semantics/ergonomics follow-ups. Nift core was not changed.

Defensible positioning: **Nift is a programmable task runner and tracked build system for authored workflows, with explicit artifact and dependency contracts.** Do not claim native cache, outputless DAG or JavaScript ecosystem feature parity.
