import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from main import classify, features

class ClassifierTests(unittest.TestCase):
    def test_detects_documentation_ip_and_login_term(self):
        result = features("http://192.0.2.44/login")
        self.assertEqual(result["has_ip_host"], 1)
        self.assertEqual(result["has_suspicious_term"], 1)

    def test_flags_synthetic_phishing_pattern(self):
        result = classify("http://verify-account.example-login-security.test")
        self.assertEqual(result["classification"], "suspicious")
        self.assertGreaterEqual(result["phishing_probability"], 0.5)

    def test_returns_clear_scope_boundary(self):
        result = classify("https://www.python.org")
        self.assertTrue(result["scope_note"].startswith("Syntax-only"))

if __name__ == "__main__":
    unittest.main()
