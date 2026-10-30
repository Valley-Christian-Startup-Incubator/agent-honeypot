import importlib.util
import io
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('eligibility', Path(__file__).with_name('check_repository.py'))
eligibility = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eligibility)
ORG = 'Valley-Christian-Startup-Incubator'
def metadata(repo='moonshine', owner=ORG):
    return {'owner': {'login': owner}, 'full_name': owner + '/' + repo,
            'html_url': 'https://github.com/' + owner + '/' + repo, 'default_branch': 'main'}

class EligibilityTests(unittest.TestCase):
    def test_common_github_remote_formats(self):
        for value in [f'https://github.com/{ORG}/moonshine.git', f'git@github.com:{ORG}/moonshine.git',
                      f'ssh://git@github.com/{ORG}/moonshine.git', f'https://github.com/{ORG.lower()}/moonshine']:
            self.assertEqual(eligibility.github_repository(value).lower(), (ORG + '/moonshine').lower())
    def test_lookalikes_and_forks_are_rejected(self):
        for value in [f'https://github.com/{ORG}-other/moonshine', f'https://github.com.evil/{ORG}/moonshine',
                      f'https://github.com/personal/{ORG}', f'https://evil@other.example/{ORG}/moonshine',
                      f'https://github.com/{ORG}/moonshine/tree/main', f'https://github.com/{ORG}/moonshine?fake=true']:
            self.assertIsNone(eligibility.github_repository(value), value)
    def test_transferred_repository_fails_owner_verification(self):
        self.assertFalse(eligibility.verified_metadata(ORG + '/moonshine', metadata(owner='personal')))
    def test_personal_origin_and_org_upstream_are_supported(self):
        remotes = f'remote.origin.url https://github.com/personal/moonshine.git\nremote.upstream.url https://github.com/{ORG}/moonshine.git\n'
        with patch.object(eligibility.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, remotes)), \
             patch.object(eligibility.urllib.request, 'urlopen', return_value=io.BytesIO(json.dumps(metadata()).encode())):
            self.assertTrue(eligibility.check('/unused')['eligible'])
    def test_no_org_remote_does_not_make_an_api_request(self):
        with patch.object(eligibility.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, 'remote.origin.url https://github.com/personal/moonshine.git\n')), \
             patch.object(eligibility.urllib.request, 'urlopen') as api:
            self.assertFalse(eligibility.check('/unused')['eligible'])
            api.assert_not_called()
    def test_unverified_metadata_does_not_enable_automation(self):
        remotes = f'remote.origin.url https://github.com/{ORG}/moonshine.git\n'
        with patch.object(eligibility.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, remotes)), \
             patch.object(eligibility.urllib.request, 'urlopen', return_value=io.BytesIO(json.dumps(metadata(owner='personal')).encode())):
            self.assertFalse(eligibility.check('/unused')['eligible'])

if __name__ == '__main__':
    unittest.main()
