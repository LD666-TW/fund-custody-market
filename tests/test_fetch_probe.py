"""更新探測遇到短暫網路錯誤應重試，持續失敗應保留錯誤。"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'pipeline'))
import fetch

class ProbeTests(unittest.TestCase):
    def run_probe(self, codes):
        with tempfile.TemporaryDirectory() as work:
            def response(cmd, **kwargs):
                code = next(codes)
                Path(cmd[cmd.index('-D')+1]).write_text('Last-Modified: Wed, 21 Oct 2026 00:00:00 GMT\r\n')
                Path(cmd[cmd.index('-o')+1]).write_bytes(b'x')
                return subprocess.CompletedProcess(cmd, code, '206 1' if code == 0 else '', 'network error')
            with patch.object(fetch, 'open_data_url', return_value='https://example.test/data.csv'), patch.object(fetch.subprocess, 'run', side_effect=response) as run, patch.object(fetch.time, 'sleep') as sleep:
                try:
                    result = fetch.probe_open_data('43476', work, log=lambda *_: None)
                    return result, run.call_count, sleep.call_count
                finally:
                    self.assertEqual(list(Path(work).iterdir()), [])

    def test_dns_and_ssl_timeout_then_success(self):
        result, calls, sleeps = self.run_probe(iter([6, 28, 0]))
        self.assertEqual((calls, sleeps), (3, 2))
        self.assertIsNotNone(result['last_modified'])

    def test_persistent_failure_is_not_reported_as_unchanged(self):
        with self.assertRaisesRegex(fetch.FetchError, '已嘗試 3 次'):
            self.run_probe(iter([6, 6, 6]))

    def test_certificate_error_is_not_retried(self):
        with self.assertRaisesRegex(fetch.FetchError, '已嘗試 1 次'):
            self.run_probe(iter([60]))

if __name__ == '__main__':
    unittest.main()
