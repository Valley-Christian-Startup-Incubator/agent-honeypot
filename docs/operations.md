# Operations

Use service-specific deployment documentation as the source of truth for its
watcher, launchd labels, release metadata, status, pause, resume, and rollback
commands. Keep those facts in the service repository rather than duplicating
mutable process IDs or port assignments here.

Before changing a running service, identify its ingress and listener, current
release, persistent data, and background jobs. Inspect selected launchd fields;
do not print entire plists or environment files. Preserve existing credentials,
saved model configuration, sessions, queue state, and user data.

Build and verify a parallel web release before switching traffic. Keep active
requests on their original process and retain browser assets across deployment
and rollback. Monitor public availability and representative authenticated
behavior. If verification fails, restore the previous route and report the
actual failure. Do not count a bot-blocked health client as application downtime.

Keep build, deploy, and recovery logs private on the host. Public repository and
HTTP discovery documents contain instructions and links only. Database
migrations, worker upgrades, shared dependencies, and model changes require their
own compatible maintenance procedure; a web deployment is not permission to
restart those components.

To refresh the shared documents, require a clean checkout and fast-forward
`main` in `~/Developer/mine/agent-honeypot`, then run:

```sh
python3 tools/install_discovery.py
```

The installer points Codex and Claude at the checked-in skill and updates the
SSH notice and home-level instruction pointers. It preserves unrelated
instructions and SSH initialization and does not change application services.
