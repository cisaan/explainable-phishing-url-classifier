# Explainable Phishing-URL Classifier

[![Tests](https://github.com/cisaan/explainable-phishing-url-classifier/actions/workflows/tests.yml/badge.svg)](https://github.com/cisaan/explainable-phishing-url-classifier/actions/workflows/tests.yml)

An offline Python project that classifies URLs as **suspicious** or **lower-risk** using transparent syntax-only features and a lightweight Bernoulli Naive Bayes model.

The tool demonstrates explainable machine learning, security-aware engineering and responsible scope boundaries. It never opens, resolves or visits the URL being analysed.

## What it demonstrates

- Feature engineering from URL syntax
- A reproducible machine-learning baseline with Laplace smoothing
- Human-readable contributing features and structured JSON output
- Safe synthetic training data using reserved domains and documentation IP ranges
- White-box and black-box testing through GitHub Actions
- Clear limitations instead of unsupported claims about whether a URL is safe

## Quick start

No third-party Python packages are required.

```bash
python src/main.py "http://verify-account.example-login-security.test"
```

Example output:

```json
{
  "url": "http://verify-account.example-login-security.test",
  "classification": "suspicious",
  "phishing_probability": 0.996,
  "observed_features": ["has suspicious term", "many hyphens"],
  "scope_note": "Syntax-only educational signal; do not use as a definitive security verdict."
}
```

Probabilities are model signals from the small embedded demonstration dataset. They are not calibrated real-world risk scores.

## Testing

```bash
python -m unittest discover -s tests -v
```

| Test type | What is checked | Result |
| --- | --- | --- |
| White-box | URL parsing, feature extraction and classification logic | Passing |
| Black-box | Command-line input and valid JSON output | Passing |
| Automated CI | Full suite on pushes and pull requests | [GitHub Actions](https://github.com/cisaan/explainable-phishing-url-classifier/actions) |

## Project structure

```text
.
├── .github/workflows/tests.yml  # cloud test workflow
├── src/main.py                  # feature extraction, model and CLI
├── tests/test_classifier.py     # white-box tests
├── tests/test_cli.py            # black-box CLI test
├── LICENSE                      # MIT licence
└── README.md
```

## Important limitations

This is an educational, syntax-only classifier. It does not use live reputation, DNS, TLS, webpage content or threat-intelligence signals. It cannot establish that a URL is safe or malicious and must not be used as the sole basis for a security decision.

Do not paste secrets, session tokens or private links into tools you do not trust. This project analyses input locally but intentionally makes no guarantee about other software or browser extensions.

## Responsible use

Use the project for learning, controlled demonstrations and defensive experimentation. Review the source, validate results independently and apply appropriate organisational security controls before adapting the approach to a real system.

## Licence

Released under the [MIT Licence](LICENSE). Feedback and responsible contributions are welcome.
