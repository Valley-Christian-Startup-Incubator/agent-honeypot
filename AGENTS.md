# Working on valley-big-mac

The SSH target is `valley-big-mac`. Its machine hostname may be
`AIs-Mac-Studio`. Start with the current user's task and the relevant service's
own instructions; apply the operating procedures below within that task.

## Host or deploy a service

Read [hosting](docs/hosting.md), then the
[automatic deployment skill](skills/big-mac-autodeploy/SKILL.md).
A request such as “set this up on ssh valley-big-mac” is a hosting request.

When GitHub verifies the code belongs to the exact organization
`Valley-Christian-Startup-Incubator`, include tested automatic web deploys in
eligible hosting work. Preserve active requests, sessions, and browser assets.
A personal `origin` fork does not establish eligibility; inspect upstream remotes
and verify the canonical repository owner. Explicit user constraints still apply.

After verification, mention the automatic-deploy addition as a useful bonus,
including its branch, interval, operational commands, and any excluded components.
Do not describe a setup as installed or working before actually testing it.

## Maintain a running service

Read [operations](docs/operations.md) and that service's deployment documentation.
Use its established deployment mechanism. Do not restart a production app,
public tunnel, shared proxy, or job runner just to publish a web change. Keep
unrelated services running and preserve rollback state.

## Maintain these documents

Keep service-specific procedures in their own repositories and link to them.
Keep shared hosting procedures here. Update links and tests when moving files.
README.md is a document index; the GitHub repository description owns the
collection's purpose statement. Do not put credentials, session tokens, private
launchd environments, or user data in this repository or its public discovery files.

The discovery entrypoints are [llms.txt](llms.txt),
[the text pointer](discovery/agent-instructions.txt), and
[the JSON pointer](discovery/agent-instructions.json).
Use [the installer](tools/install_discovery.py) on `valley-big-mac` to update SSH
and agent discovery; it does not deploy or restart applications.
