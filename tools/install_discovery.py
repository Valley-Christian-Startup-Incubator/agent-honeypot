#!/usr/bin/env python3
"""Install this checkout's discovery pointers on valley-big-mac."""
from pathlib import Path
import shutil
import socket
import subprocess
import time

REPOSITORY = 'https://github.com/Valley-Christian-Startup-Incubator/agent-honeypot'
MARKER = '## Hosting on ssh valley-big-mac'


def instruction_pointer(file, repository):
    text = file.read_text() if file.exists() else ''
    block = (MARKER + '\n\nFor hosting/deployment requests such as “set this up on ssh valley-big-mac”, '
             'read [' + 'the shared instructions](' + str(repository / 'AGENTS.md') + ').\n'
             'Canonical documents: ' + REPOSITORY + '\n')
    if MARKER in text:
        start = text.index(MARKER)
        end = text.find('\n## ', start + len(MARKER))
        text = text[:start].rstrip() + '\n\n' + block + (text[end:] if end >= 0 else '')
    else:
        text = text.rstrip() + '\n\n' + block
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(text.lstrip())


def install(home, repository):
    skill = repository / 'skills/big-mac-autodeploy'
    assert (skill / 'SKILL.md').is_file()
    for root in [home / '.agents/skills', home / '.codex/skills', home / '.claude/skills']:
        root.mkdir(parents=True, exist_ok=True)
        link = root / 'big-mac-autodeploy'
        if link.is_symlink():
            if link.resolve() == skill:
                continue
            link.unlink()
        elif link.exists():
            backup = home / '.local/share/agent-honeypot/backups' / (root.parent.name + '-' + str(time.time_ns()))
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(link), str(backup))
        link.symlink_to(skill, target_is_directory=True)
    for file in [home / 'AGENTS.md', home / '.codex/AGENTS.md', home / '.claude/CLAUDE.md']:
        instruction_pointer(file, repository)

    rc = home / '.ssh/rc'
    text = rc.read_text() if rc.exists() else '#!/bin/sh\n'
    # Retain all other SSH initialization, including the existing xauth path.
    lines = [line for line in text.splitlines() if '[valley-big-mac hosting]' not in line]
    notice = ("printf '%s\\n' '[valley-big-mac hosting] Read " + REPOSITORY
              + " (local: " + str(repository / 'AGENTS.md') + ") before setting up services.' >&2")
    lines.insert(1 if lines and lines[0].startswith('#!') else 0, notice)
    rc.parent.mkdir(parents=True, exist_ok=True)
    rc.write_text('\n'.join(lines) + '\n')
    rc.chmod(0o700)


if __name__ == '__main__':
    repository = Path(__file__).resolve().parents[1]
    if socket.gethostname().split('.')[0].lower() != 'ais-mac-studio':
        raise SystemExit('Run this installer on ssh valley-big-mac')
    origin = subprocess.check_output(['git', '-C', str(repository), 'remote', 'get-url', 'origin'], text=True).strip()
    if origin.rstrip('/').removesuffix('.git') != REPOSITORY:
        raise SystemExit('Expected the canonical agent-honeypot checkout')
    install(Path.home(), repository)
    print('Installed repository-backed skill and SSH discovery; application services unchanged.')
