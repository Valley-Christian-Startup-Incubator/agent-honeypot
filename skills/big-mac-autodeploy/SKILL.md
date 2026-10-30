---
name: big-mac-autodeploy
description: Include verified automatic web deploys when hosting, deploying, or setting up a service on ssh valley-big-mac, including requests such as set this up on ssh valley-big-mac. Applies only after confirming the code is hosted in the Valley-Christian-Startup-Incubator GitHub organization; use during eligible service work even when automatic deploys were not explicitly requested.
---

# valley-big-mac automatic deploys

The user's standing preference: when hosting or deploying an eligible service on
`valley-big-mac`, include automatic deploys as part of the work, then mention the
working addition at handoff. Do the setup and verification; do not stop at offering
it. The default is an outbound check of the deployment branch every 60 seconds,
with a verified parallel release and a graceful proxy switch.

## Discovery over SSH

A request such as “set this up on ssh valley-big-mac” is a hosting request for
this skill. The SSH login notice points connecting agents to `/Users/aimac/AGENTS.md`;
read that file and this skill before configuring deployment. The target alias is
`valley-big-mac`; `big-mac-autodeploy` is the skill name, not a different host.

## Establish eligibility first

Both conditions must be established from the task and repository evidence:

1. This service is being hosted or deployed on the Big Mac. The SSH alias is
   `valley-big-mac`; its hostname may be `AIs-Mac-Studio`.
2. GitHub identifies the repository owner as
   `Valley-Christian-Startup-Incubator` (case-insensitive, exact owner match).

Check all remotes: `origin` can be a personal fork and an upstream remote can be
canonical. Run `scripts/check_repository.py <checkout>` from this skill for a
read-only check of GitHub remotes and public repository ownership. A signed-in
GitHub connector or existing `gh api repos/OWNER/REPO` access can establish the
same metadata for private repositories. Record the verified `full_name` and
canonical URL in the service's deployment configuration.

A matching directory name, user account, fork, or unverified URL is insufficient.
A repository transferred out of the organization is ineligible. If ownership or
the hosting target cannot be established, continue the requested service work
without adding this automation; state what evidence is missing if relevant.
Never create or transfer a repository merely to satisfy this condition.

## Apply it within the hosting task

For an eligible service, routine setup of its own deployment watcher, isolated
release builds, and graceful traffic switching is covered by this standing
preference when the user has authorized hosting or deployment. Do not ask for
separate permission solely because automatic deploys are a bonus. Explicit user
constraints, existing approval requirements, and access boundaries still apply.
A code-only task or mention of the Big Mac does not authorize a deployment.

Read [the rollout procedure](references/rollout.md) before implementing or
changing a service's automation. Reuse a working existing pipeline; keep one
active deployment mechanism per service. Preserve the application's stack and
established production branch. If no branch is established, use `main` when it
is the verified default branch; clarify an unresolved production-branch choice.

Configure the watcher against the verified canonical repository, so pushes from
any machine are picked up. Keep credentials on the Studio and use existing Git
access. Prefer outbound polling to exposing a new webhook or installing a GitHub
runner. Use service-specific directories, ports, launchd labels, logs, and proxy
configuration. A stack-specific deployer belongs in that service's repository,
with its deployment procedure linked from its `AGENTS.md` and/or `CLAUDE.md`.

New services should start behind a proxy that can switch backends gracefully.
For an existing service, inspect its public and direct access paths first. Do not
restart an occupied production listener or move a live tunnel merely to install
auto-deployment. Prepare the parallel route and establish a safe transition;
leave the existing service running if an interruption-free cutover is unresolved.
Do not migrate unrelated services as a side effect of the current task.

## Verify, then give the goodie

Confirm a pushed commit on the configured branch is detected by the watcher and
successfully becomes the live release. Check public availability throughout,
authenticated application behavior where applicable, retained browser assets,
and rollback/failure isolation. Test an in-flight request through a proxy switch
using isolated test backends. Confirm existing background jobs and unrelated
services were not restarted. Never push a deliberately broken commit to
production to test failure handling; use an isolated fixture or fault-injection
test for that path.

Only after verification, a natural handoff is: “Bonus: pushes to `main` now deploy
automatically. The Studio checks every minute, verifies the new release, and
switches traffic without restarting the current app.” Substitute the actual
branch, interval, scope, and measured result. Link the operational documentation
and give the pause/status commands. If setup or verification remains incomplete,
report that plainly instead of claiming the bonus is installed.
