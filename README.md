# Explainable Phishing-URL Classifier

An offline Python learning project that classifies URLs as **suspicious** or **lower-risk** using transparent syntax-only features and a small Bernoulli Naive Bayes model.

## What it demonstrates

- Feature engineering from URL syntax without opening, resolving, or visiting URLs
- A reproducible machine-learning baseline with Laplace smoothing
- Structured JSON results with human-readable contributing features
- Safe synthetic training data, unit tests, and GitHub Actions CI

## Run it

```bash
python src/main.py "http://verify-account.example-login-security.test"
python -m unittest discover -s tests -v
```

## Important limitations

This is an educational, syntax-only classifier. It does not visit URLs or use live reputation, DNS, TLS, content, or threat-intelligence signals. It cannot establish that a URL is safe or malicious and must not be used as the sole basis for a security decision.

All suspicious examples use reserved `.test` domains and documentation IP ranges.
