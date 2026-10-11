# Participant investigation

Proposed primary set: Nift, Turborepo, Nx. Nift supplies procedural `.f` plus tracked artifact scheduling. Turbo supplies package/task pipelines and cache-oriented execution. Nx supplies project/target graphs, explicit inputs/outputs and tooling. Make/Ninja are excluded as primary participants: they have a separate campaign.

Just is a useful qualitative contrast for authored recipes, but is not assumed to offer equivalent incremental state and bounded parallel DAG execution. Include it quantitatively only if native equivalent contracts can be certified without an adapter scheduler; otherwise keep three primary participants.

Official sources checked 11 October 2026:
- https://turborepo.dev/docs/reference/configuration
- https://turborepo.dev/docs/crafting-your-repository/configuring-tasks
- https://nx.dev/docs/reference/project-configuration
- https://nx.dev/docs/reference/inputs
- https://nx.dev/docs/reference/nx-json
- https://nx.dev/docs/concepts/how-caching-works
- https://just.systems/man/en/

Nx separates prerequisite ordering from hashed inputs too; that distinction is meaningful, not inherently redundant ceremony. Turbo/Nx restore cached outputs and replay logs. Initial hypotheses must be tested against pinned installations. Versions are not frozen yet.
