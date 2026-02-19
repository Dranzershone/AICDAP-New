
import re
from urllib.parse import urlparse
import math
from collections import Counter

def url_features(url: str) -> list:
    parsed = urlparse(url)
    netloc = parsed.netloc or ''
    # crude subdomain length as number of dots in netloc before registered domain approximation
    subdomain_len = max(0, netloc.count('.') - 1)
    length = len(url)
    num_dots = url.count('.')
    num_hyphens = url.count('-')
    path_len = len(parsed.path)
    has_at = 1 if '@' in url else 0
    punycode = 1 if 'xn--' in url else 0
    has_ip = 1 if re.match(r'^\d+\.\d+\.\d+\.\d+$', netloc) else 0
    digits = sum(c.isdigit() for c in url)
    entropy = shannon_entropy(url)

    return [length, num_dots, num_hyphens, path_len, has_at, punycode, has_ip, subdomain_len, digits, entropy]

def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    counts = Counter(s)
    probs = [c / len(s) for c in counts.values()]
    return -sum(p * math.log2(p) for p in probs)
