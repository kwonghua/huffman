import math
from collections import Counter

def calculate_entropy(text):
    if not text:
        return 0
    counts = Counter(text)
    total_chars = len(text)

    entropy = 0
    for count in counts.values():
        p = count / total_chars
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy
