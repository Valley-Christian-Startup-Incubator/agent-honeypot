# Automatic deployment on the Big Mac

Use this procedure after the eligibility gate in `SKILL.md`. Adapt build and
health commands to the actual service; avoid copying Moonshine's app-specific
paths, data checks, ports, or credentials into another project.

## Discover the current deployment

Identify the canonical GitHub repository, production branch, source checkout,
public hostname, runtime, data directories, service manager, and ingress route.
Inspect only the launchd fields needed for that inventory; never print an entire
plist or environment file. Check listeners and existing proxy routes before
allocating service-specific ports. Keep existing secrets and persistent data
outside release directories.

Reuse an existing healthy auto-deployer instead of adding a second watcher. For
Moonshine, use its own `scripts/deploy_web.py` and
`docs/zero-downtime-deployment.md` at
`/Users/aimac/Developer/mine/moonshine`. That implementation is a working design
reference for other services, not a generic installer: its health checks, source
repository, model checks, port range, and service paths are Moonshine-specific.

Choose a dedicated service namespace, such as `com.incubator.<service>.*`, and a
runtime root outside the checkout, such as `~/.local/share/<service>/deploy`.
Give the service its own proxy configuration or change only its route in an
existing proxy. Preserve shared Caddy settings, admin listeners, routes, and
application processes. When running a dedicated Caddy instance, isolate its
config storage or disable autosave so it cannot overwrite another instance's
saved configuration.

## Watch the verified deployment branch

Install a per-service launchd job using `RunAtLoad`, `StartInterval: 60`, and a
nonblocking deployment lock shared by manual and automatic runs. Use the actual
launchd domain on the host; existing classroom jobs use `user/501`, not a GUI
domain. Keep log output quiet when the branch is unchanged. Installing or updating
a watcher must acquire the same lock before unloading an earlier watcher, so it
cannot interrupt a deployment in progress.

Fetch the verified canonical repository explicitly. Require a clean checkout and
fast-forward history, and refuse dirty files or force-pushed divergence without
discarding work. Never deploy another branch just because it has newer commits.
A build failure should record the commit and a private diagnostic log, leave the
active release untouched, and avoid retrying the same broken commit every minute.
A new commit or an explicit manual retry can initiate another attempt.

Store build scripts, reproducible dependency locks, health checks, and deployment
instructions in the service's repository. Pin the watcher to a tested version;
update its installed copy only after a successful rollout. Document how to update
the deployer itself if a fix must take effect before the next rollout.

## Build and switch without interrupting users

Build each attempt into a separate immutable directory and launch it on a free
loopback port. Reuse the service's saved environment and shared session/data
locations without logging secrets. Run relevant checks before the candidate
receives public traffic. Repeated builds should have lower scheduling priority
where practical and must not restart classroom training or other background jobs.

Publish hashed browser assets from both versions to an append-only location
served by the proxy before switching, so both forward deployment and rollback
support open tabs. Publish each new asset atomically; never truncate or rewrite
an asset currently being served. Retain any other versioned client resources the
application needs. Keep the previous app running for requests and rollback.

Verify local readiness, dependencies, and representative application behavior,
including authentication and data access when applicable. Use temporary test
sessions where appropriate; avoid sending user messages, modifying real records,
or launching paid jobs as a health probe. Test the public health monitor before
cutover: a probe blocked by bot protection does not establish application health.

Persist the previous release and proxy configuration before an atomic graceful
switch. Keep startup configuration and the active release pointer consistent.
Monitor the public route continuously, repeat application checks through that
route, and restore the previous upstream on failure. Record transaction state so
an interrupted switch can be recovered safely before another attempt. Check the
proxy's actual behavior for long responses and any streaming/WebSocket traffic;
“graceful reload” alone is not proof that every protocol's connections survive.

After a failed cutover, let the candidate finish its in-flight requests before
retiring it. Keep the active and rollback processes; stop only older managed
processes that have drained. Bound process accumulation without deleting assets
needed by existing tabs. Release and log retention needs to suit available disk
space and the service's rollback window.

An auto-deployer for the web process must not silently run database migrations,
replace model files, restart queue workers, or update shared system dependencies.
State that scope in the handoff and deployment docs. Handle necessary persistent
schema changes with a separately established compatible migration procedure.

## Prove the trigger and document operations

Install the watcher while the production branch is unchanged, then push a real,
reviewed service change and let the watcher detect it. Verify the live commit,
public checks, application checks, preserved assets, and unchanged unrelated
service processes. Use an isolated proxy/backend test for in-flight request
continuity and isolated tests for build failures, rollback, recovery, and locking.
If a real push cannot be authorized within the task, leave trigger verification
marked pending; do not create an empty production commit just for appearances.

Keep the following in the service's checked-in operational documentation:

- Canonical repository, watched branch, interval, public route, and app scope.
- Deployer path, runtime root, launchd label/domain, and private log locations.
- Status and immediate-deploy commands, plus pause/resume commands that do not
  stop an in-progress deployment.
- Active/previous release state, rollback command or procedure, failure retry
  policy, and how to recover an interrupted switch.
- What remains outside the auto-deployer: migrations, workers, and host upgrades.

Link this operational procedure from the repository's agent instructions so a
future agent uses the same route instead of restarting the live service.
