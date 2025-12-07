from entropy import calculate_entropy

def analyze_file(filename):
    with open(filename, "r") as f:
        text = f.read()

    entropy = calculate_entropy(text)
    bits_per_char = entropy
    theoretical_min_bits = entropy * len(text)

    print(f"File: {filename}")
    print(f"  Entropy (bits/char): {bits_per_char:.4f}")
    print(f"  Theoretical Minimum: {theoretical_min_bits:.2f} bits")
    print(f"  Equivalent Size: {theoretical_min_bits/8:.2f} bytes")
    print()


# analyze_file("random.txt")
