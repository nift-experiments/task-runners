r := cmd("python3", "task_body.py", "unit-test").run()
if(!r.launched || r.exit_code != 0) { throw error(r.stderr, "user.task.failed") }
