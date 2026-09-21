import json
import subprocess
import sys
import unittest
from pathlib import Path

APP = Path(__file__).parents[1] / "src" / "main.py"

class CommandLineTests(unittest.TestCase):
    def test_cli_returns_suspicious_result_for_safe_synthetic_case(self):
        completed = subprocess.run([sys.executable, str(APP), "http://verify-account.example-login-security.test"], capture_output=True, text=True, check=True)
        result = json.loads(completed.stdout)
        self.assertEqual(result["classification"], "suspicious")
        self.assertIn("scope_note", result)

    def test_cli_returns_valid_json_for_lower_risk_example(self):
        completed = subprocess.run([sys.executable, str(APP), "https://www.python.org"], capture_output=True, text=True, check=True)
        self.assertIn("classification", json.loads(completed.stdout))

if __name__ == "__main__":
    unittest.main()
