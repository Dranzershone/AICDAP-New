import re
import math
from urllib.parse import urlparse
from collections import Counter


def url_features(url: str) -> list:
    """
    Extract numerical features from a URL for phishing detection.
    Handles malformed URLs safely.
    """

    try:
        # Ensure URL is string
        if not isinstance(url, str):
            return default_features()

        parsed = urlparse(url)

        netloc = parsed.netloc or ""
        path = parsed.path or ""

        # Subdomain estimation
        subdomain_len = max(0, netloc.count(".") - 1)

        # Basic features
        length = len(url)
        num_dots = url.count(".")
        num_hyphens = url.count("-")
        path_len = len(path)

        # Suspicious patterns
        has_at = 1 if "@" in url else 0
        punycode = 1 if "xn--" in url else 0

        # Detect IPv4
        has_ip = 1 if re.match(r"^\d+\.\d+\.\d+\.\d+$", netloc) else 0

        # Count digits
        digits = sum(c.isdigit() for c in url)

        # Entropy
        entropy = shannon_entropy(url)

        return [
            length,
            num_dots,
            num_hyphens,
            path_len,
            has_at,
            punycode,
            has_ip,
            subdomain_len,
            digits,
            entropy,
        ]

    except Exception:
        # If URL parsing fails (invalid IPv6 etc.)
        return default_features()


def default_features():
    """
    Default feature vector used when URL parsing fails.
    Keeps model training stable.
    """
    return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def shannon_entropy(s: str) -> float:
    """
    Compute Shannon entropy of a string.
    """
    if not s:
        return 0.0

    counts = Counter(s)
    probs = [c / len(s) for c in counts.values()]

    return -sum(p * math.log2(p) for p in probs)