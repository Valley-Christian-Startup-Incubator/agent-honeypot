#!/usr/bin/env python3
"""Read-only eligibility check for public Incubator GitHub repositories.

Private repositories can be verified using an existing authenticated GitHub tool;
this helper never requests, reads, or prints access tokens.
"""
import argparse
import json
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request

ORG = 'valley-christian-startup-incubator'


def github_repository(url):
    url = url.strip()
    if url.startswith('git@github.com:'):
        path = url[len('git@github.com:'):]
    else:
        try:
            parsed = urllib.parse.urlsplit(url)
            if parsed.hostname != 'github.com' or parsed.scheme not in ('https', 'ssh'):
                return None
            if parsed.query or parsed.fragment:
                return None
            if parsed.port not in (None, 22, 443):
                return None
            if parsed.scheme == 'ssh' and parsed.username != 'git':
                return None
            path = parsed.path.lstrip('/')
        except ValueError:
            return None
    path = path.rstrip('/')
    if path.endswith('.git'):
        path = path[:-4]
    parts = path.split('/')
    if len(parts) != 2 or not all(re.fullmatch(r'[A-Za-z0-9_.-]+', part) for part in parts):
        return None
    if parts[0].lower() != ORG or parts[1] in ('.', '..'):
        return None
    return '/'.join(parts)


def verified_metadata(candidate, metadata):
    expected_owner, expected_repo = candidate.split('/')
    return (metadata.get('owner', {}).get('login', '').lower() == ORG
            and metadata.get('full_name', '').lower() == (expected_owner + '/' + expected_repo).lower()
            and metadata.get('html_url', '').lower() == ('https://github.com/' + candidate).lower()
            and bool(metadata.get('default_branch')))


def check(checkout):
    remotes = subprocess.run(['git', '-C', checkout, 'config', '--get-regexp', r'^remote\..*\.url$'],
                             capture_output=True, text=True)
    if remotes.returncode not in (0, 1):
        return {'eligible': False, 'reason': 'Cannot read repository remotes'}
    candidates = sorted({value for line in remotes.stdout.splitlines()
                         if len(line.split(None, 1)) == 2
                         for value in [github_repository(line.split(None, 1)[1])] if value})
    if not candidates:
        return {'eligible': False, 'reason': 'No GitHub remote in the required organization'}
    verified = []
    for candidate in candidates:
        request = urllib.request.Request('https://api.github.com/repos/' + candidate,
                                         headers={'Accept': 'application/vnd.github+json',
                                                  'User-Agent': 'big-mac-autodeploy-eligibility'})
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                metadata = json.load(response)
            if verified_metadata(candidate, metadata):
                verified.append({'full_name': metadata['full_name'], 'url': metadata['html_url'],
                                 'default_branch': metadata['default_branch']})
        except (urllib.error.URLError, ValueError):
            continue
    if not verified:
        return {'eligible': False, 'reason': 'Ownership not verified; use existing authenticated GitHub access for private repositories'}
    if len(verified) > 1:
        return {'eligible': False, 'reason': 'Multiple organization repositories; identify the service canonical repository',
                'verified_candidates': verified}
    return {'eligible': True, 'repository': verified[0]}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkout')
    args = parser.parse_args()
    result = check(args.checkout)
    print(json.dumps(result))
    raise SystemExit(0 if result['eligible'] else 1)
