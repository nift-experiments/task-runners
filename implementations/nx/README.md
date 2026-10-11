# Nx adapter

See `generators/workflow.py`: one project with native `nx:run-commands` targets, explicit ordering, own/config/body inputs, dependent task output inputs and outputs. Each fixture has an isolated local cache directory. Nx daemon/cloud are disabled for fresh CLI measurements. Native Nx schedules tasks; no adapter scheduler.
