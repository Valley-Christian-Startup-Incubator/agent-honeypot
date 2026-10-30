# Hosting a service

Connect with `ssh valley-big-mac` and read `~/AGENTS.md`. The shared checkout is
`~/Developer/mine/agent-honeypot`. Its source is
<https://github.com/Valley-Christian-Startup-Incubator/agent-honeypot>.

Identify the requested service, its repository, runtime, production branch,
persistent data, and public access path. For an existing service, inspect its
current deployment before changing it. A hosting request covers setting up that
service; it does not authorize changing unrelated apps or publishing secrets.

Use [big-mac-autodeploy](../skills/big-mac-autodeploy/SKILL.md) to establish
GitHub ownership and configure automatic deploys for eligible services. The exact
owner must be `Valley-Christian-Startup-Incubator`. Personal forks and similarly
named organizations do not qualify. If verification is unavailable, finish the
hosting work you can and report what remains unverified.

Use isolated releases, a service-specific watcher, and a proxy that can switch
backends without dropping active requests. Keep one deployment mechanism per
service. Follow the [rollout procedure](../skills/big-mac-autodeploy/references/rollout.md)
for health checks, retained browser assets, rollback, recovery, and verification.

When configuring a public HTTP service within the hosting task, make the
collection discoverable through `/llms.txt` and
`/.well-known/agent-instructions` (optionally the JSON variant). Reuse the files
in `discovery/` and the root `llms.txt`, or link to their canonical GitHub URLs.
Preserve existing discovery documents by merging useful links; never replace
service documentation, robots policies, authentication, or unrelated proxy routes.
Only publish the public document pointers, not host files or environment data.

For Moonshine, its live configuration and deployer are documented in
[Moonshine's deployment procedure](https://github.com/Valley-Christian-Startup-Incubator/moonshine/blob/main/docs/zero-downtime-deployment.md).
Do not copy Moonshine's ports, source paths, model checks, or credentials to a
new service.
