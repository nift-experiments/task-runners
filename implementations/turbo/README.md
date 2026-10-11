# Turbo adapter

See `generators/workflow.py`: ordinary single-package npm scripts, explicit same-package `dependsOn`, own/config/body/consumed-artifact inputs and per-task outputs. Native Turbo schedules tasks. Remote cache is disabled; local read/write cache is explicit. Cache-disabled execution uses `--cache=local:`. Commands and declared scope are retained per observation.
