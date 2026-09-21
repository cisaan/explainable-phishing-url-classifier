"""Offline, explainable phishing-URL classifier.

The tool never opens, resolves or visits the supplied URL. It analyses URL syntax
only and is an educational signal—not a definitive security verdict.
"""

from __future__ import annotations

import argparse
import json
import math
from urllib.parse import urlparse

TERMS = ("login", "verify", "secure", "update", "account", "wallet", "signin")
TRAINING = [
    ("https://www.gov.uk", 0),
    ("https://www.python.org/downloads", 0),
    ("https://www.bbc.co.uk/news", 0),
    ("https://docs.python.org/3/", 0),
    ("https://www.openstreetmap.org", 0),
    ("https://support.example.org/help", 0),
    ("http://verify-account.example-login-security.test", 1),
    ("http://192.0.2.44/login/verify", 1),
    ("https://secure-update-account.example.test", 1),
    ("http://signin.example.test@198.51.100.8/login", 1),
    ("https://xn--secure-login-9db.example.test", 1),
    ("https://verify-wallet-access.example.test", 1),
]


def features(url):
    raw = url.strip()
    parsed = urlparse(raw if "://" in raw else "https://" + raw)
    host = (parsed.hostname or "").lower()
    parts = [part for part in host.split(".") if part]
    ip_host = len(parts) == 4 and all(
        part.isdigit() and 0 <= int(part) <= 255 for part in parts
    )
    lowered = raw.lower()
    return {
        "uses_https": int(parsed.scheme == "https"),
        "long_url": int(len(raw) >= 75),
        "many_subdomains": int(len(parts) >= 4),
        "has_ip_host": int(ip_host),
        "has_at_symbol": int("@" in raw),
        "has_punycode": int("xn--" in host),
        "has_suspicious_term": int(any(term in lowered for term in TERMS)),
        "many_hyphens": int(host.count("-") >= 2),
        "has_encoded_chars": int("%" in raw),
    }


def fit(rows):
    names = tuple(features(rows[0][0]))
    counts = {0: 0, 1: 0}
    positive = {name: {0: 0, 1: 0} for name in names}
    for url, label in rows:
        counts[label] += 1
        for name, value in features(url).items():
            positive[name][label] += value
    probabilities = {
        name: (
            (positive[name][0] + 1) / (counts[0] + 2),
            (positive[name][1] + 1) / (counts[1] + 2),
        )
        for name in names
    }
    return (counts[1] + 1) / (len(rows) + 2), probabilities


def classify(url):
    prior, probabilities = fit(TRAINING)
    safe_score = math.log(1 - prior)
    phishing_score = math.log(prior)
    observed = []
    for name, value in features(url).items():
        safe_probability, phishing_probability = probabilities[name]
        safe_score += math.log(safe_probability if value else 1 - safe_probability)
        phishing_score += math.log(
            phishing_probability if value else 1 - phishing_probability
        )
        if value and name != "uses_https":
            observed.append(name.replace("_", " "))
    probability = 1 / (1 + math.exp(safe_score - phishing_score))
    return {
        "url": url,
        "classification": "suspicious" if probability >= 0.5 else "lower-risk",
        "phishing_probability": round(probability, 3),
        "observed_features": observed or ["no high-risk syntax features observed"],
        "scope_note": (
            "Syntax-only educational signal; do not use as a definitive security verdict."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Offline explainable phishing-URL classifier"
    )
    parser.add_argument("url", help="URL to inspect; it is never visited")
    print(json.dumps(classify(parser.parse_args().url), indent=2))
