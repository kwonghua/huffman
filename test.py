import time
import math
import os
import sys
import huffman 
from entropy import calculate_entropy
from lzw import LZW
from fixedlength import FixedLength
import random
import string
from io import StringIO

# Matplotlib not needed - graphs are optional

# --- Main Test Execution ---

def run_tests():
    """Runs tests on different file types and compares compression ratios."""
    # NOTE: Ensure these files (wikipedia.txt, random.txt, etc.) exist in the same directory!
    files = ["wikipedia.txt", "random.txt", "equal_dist.txt", "single_char.txt"]
    
    # Create a simple file for testing the single-character edge case
    with open("single_char.txt", 'w') as f:
        f.write("A" * 500)
    
    print("\n" + "=" * 140)
    print("Compression Comparison: Huffman vs LZW (with Entropy & FixedLength Baseline)")
    print("=" * 140)
    
    # Print table header with all methods
    print(
        f"{'File':<18} | {'Original':<12} | {'Entropy':<12} | "
        f"{'Huffman':<12} | {'Huff Ratio':<12} | "
        f"{'LZW':<12} | {'LZW Ratio':<12} | "
        f"{'Fixed':<12} | {'Fixed Ratio':<12} | "
        f"{'Integrity':<10}"
    )
    print("-" * 140)
    
    for filename in files:
        # --- 1. Load Original Data ---
        try:
            # Use UTF-8 encoding to correctly read common text files
            with open(filename, 'r', encoding='utf-8') as f:
                original_text = f.read()
        except FileNotFoundError:
            print(f"{filename:<18} | File not found. Skipping.")
            continue
            
        original_bits = len(original_text.encode('utf-8')) * 8 
        
        # --- 2. Calculate Entropy (Theoretical Minimum) ---
        entropy_per_char = calculate_entropy(original_text)
        entropy_bits = entropy_per_char * len(original_text)
        
        # --- 3. Run Huffman Compression and Decompression ---
        huff_output_file = "temp_huffman.bin"
        
        try:
            huffman_data_bits = huffman.compress_to_file(original_text, huff_output_file)
        except Exception as e:
            print(f"Error during Huffman compression for {filename}: {e}")
            huffman_data_bits = 0
            huffman_decompressed = ""

        # Calculate Huffman Ratio
        huff_ratio = original_bits / huffman_data_bits if huffman_data_bits > 0 else 0.0

        # Decompress and verify Huffman
        huff_intact = "N/A"
        if huffman_data_bits > 0:
            try:
                huffman_decompressed = huffman.decompress_from_file(huff_output_file)
                huff_intact = "PASS" if huffman_decompressed == original_text else "FAIL"
            except Exception as e:
                huff_intact = "ERROR"
        
        # --- 4. Run LZW Compression ---
        lzw_bits = 0
        lzw_ratio = 0.0
        lzw_intact = "N/A"
        try:
            lzw_codes = LZW.encode(original_text)
            lzw_bits = LZW.get_size_bits(lzw_codes)
            lzw_ratio = original_bits / lzw_bits if lzw_bits > 0 else 0.0
            
            # Verify LZW integrity
            lzw_decompressed = LZW.decode(lzw_codes)
            lzw_intact = "PASS" if lzw_decompressed == original_text else "FAIL"
        except Exception as e:
            lzw_bits = 0
            lzw_ratio = 0.0
            lzw_intact = "ERROR"
            print(f"Error during LZW compression for {filename}: {type(e).__name__}: {e}")
        
        # Combined integrity check
        if huff_intact == "PASS" and lzw_intact == "PASS":
            is_intact = "PASS"
        elif huff_intact == "FAIL" or lzw_intact == "FAIL":
            is_intact = "FAIL"
        else:
            is_intact = f"H:{huff_intact} L:{lzw_intact}"
        
        # --- 5. Run FixedLength Baseline ---
        fixed_bits = FixedLength.get_size_in_bits(original_text)
        fixed_ratio = original_bits / fixed_bits if fixed_bits > 0 else 0.0
        
        # --- 6. Print Results ---
        print(
            f"{filename:<18} | "
            f"{original_bits:<12} | "
            f"{entropy_bits:<12.1f} | "
            f"{huffman_data_bits:<12} | "
            f"{huff_ratio:<12.2f} | "
            f"{lzw_bits:<12} | "
            f"{lzw_ratio:<12.2f} | "
            f"{fixed_bits:<12} | "
            f"{fixed_ratio:<12.2f} | "
            f"{is_intact:<10}"
        )

    print("-" * 140)
    
    # Print summary statistics
    print("\nSummary:")
    print("  - Entropy: Theoretical minimum bits (Shannon's source coding theorem)")
    print("  - Huffman: Optimal prefix coding based on character frequencies")
    print("  - LZW: Dictionary-based compression (adaptive, builds dictionary on-the-fly)")
    print("  - Fixed: Baseline ASCII encoding (8 bits per character)")
    print("  - Ratio: Original size / Compressed size (higher is better)")
    print("\nNote: This comparison focuses on Huffman vs LZW, two major compression algorithms.")
    
    # Cleanup temporary files
    if os.path.exists("temp_huffman.bin"):
        os.remove("temp_huffman.bin")
    if os.path.exists("single_char.txt"):
        os.remove("single_char.txt")
    print("\nCleanup complete.")

# --- Time Complexity Analysis ---

def generate_random_file(filename, size):
    """Generates a random text file of specified size."""
    chars = string.ascii_letters + string.digits + ' ' + string.punctuation
    random_text = ''.join(random.choice(chars) for _ in range(size))
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(random_text)
    return len(random_text)

def test_time_complexity():
    """Tests compression rates for random files at different sizes."""
    print("\n" + "=" * 140)
    print("Compression Rate Analysis: Random files Compression Rate vs Input Size")
    print("=" * 140)
    
    sizes = [10000, 50000, 100000]  # 10k, 50k, 100k
    huffman_ratios = []
    lzw_ratios = []
    file_sizes = []
    
    print(f"\n{'Size (chars)':<15} | {'Original':<12} | {'Huffman':<12} | {'Huff Ratio':<12} | {'LZW':<12} | {'LZW Ratio':<12}")
    print("-" * 80)
    
    for size in sizes:
        filename = f"temp_random_{size}.txt"
        
        # Generate random file
        actual_size = generate_random_file(filename, size)
        file_sizes.append(actual_size)
        
        # Read the file
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
        
        original_bits = len(text.encode('utf-8')) * 8
        
        # Test Huffman compression
        huff_output = f"temp_huff_{size}.bin"
        try:
            # Suppress print output
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            huffman_bits = huffman.compress_to_file(text, huff_output)
            sys.stdout = old_stdout
            huff_ratio = original_bits / huffman_bits if huffman_bits > 0 else 0.0
        except Exception as e:
            sys.stdout = old_stdout
            print(f"Error in Huffman compression: {e}")
            huffman_bits = 0
            huff_ratio = 0.0
        huffman_ratios.append(huff_ratio)
        
        # Test LZW compression
        try:
            lzw_codes = LZW.encode(text)
            lzw_bits = LZW.get_size_bits(lzw_codes)
            lzw_ratio = original_bits / lzw_bits if lzw_bits > 0 else 0.0
        except Exception as e:
            print(f"Error in LZW compression: {e}")
            lzw_bits = 0
            lzw_ratio = 0.0
        lzw_ratios.append(lzw_ratio)
        
        print(f"{actual_size:<15} | {original_bits:<12} | {huffman_bits:<12} | {huff_ratio:<12.2f} | {lzw_bits:<12} | {lzw_ratio:<12.2f}")
        
        # Cleanup
        if os.path.exists(filename):
            os.remove(filename)
        if os.path.exists(huff_output):
            os.remove(huff_output)
    
    print("-" * 80)
    
    # Print analysis
    print("\nCompression Rate Analysis (Random files):")
    if len(huffman_ratios) >= 2:
        size_ratio = file_sizes[-1] / file_sizes[0] if file_sizes[0] > 0 else 0
        print(f"  - Size increased by {size_ratio:.1f}x ({file_sizes[0]:,} -> {file_sizes[-1]:,} characters)")
        if huffman_ratios[0] > 0:
            print(f"  - Huffman compression ratio: {huffman_ratios[0]:.2f}x -> {huffman_ratios[-1]:.2f}x")
        if lzw_ratios[0] > 0:
            print(f"  - LZW compression ratio: {lzw_ratios[0]:.2f}x -> {lzw_ratios[-1]:.2f}x")
    
    print("\nRandom files compression rate analysis complete.")

def test_wikipedia_time_complexity():
    """Tests compression rates for Wikipedia files at different sizes."""
    print("\n" + "=" * 140)
    print("Compression Rate Analysis: Wikipedia files Compression Rate vs Input Size")
    print("=" * 140)
    
    wikipedia_files = ["wikipedia_50k.txt", "wikipedia.txt", "wikipedia_200k.txt"]
    huffman_ratios = []
    lzw_ratios = []
    file_sizes = []
    
    print(f"\n{'File':<20} | {'Size (chars)':<15} | {'Original':<12} | {'Huffman':<12} | {'Huff Ratio':<12} | {'LZW':<12} | {'LZW Ratio':<12}")
    print("-" * 100)
    
    for filename in wikipedia_files:
        if not os.path.exists(filename):
            print(f"{filename:<20} | File not found. Skipping.")
            continue
        
        # Read the file
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
        
        actual_size = len(text)
        file_sizes.append(actual_size)
        original_bits = len(text.encode('utf-8')) * 8
        
        # Test Huffman compression
        huff_output = f"temp_huff_{filename}.bin"
        try:
            # Suppress print output
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            huffman_bits = huffman.compress_to_file(text, huff_output)
            sys.stdout = old_stdout
            huff_ratio = original_bits / huffman_bits if huffman_bits > 0 else 0.0
        except Exception as e:
            sys.stdout = old_stdout
            print(f"Error in Huffman compression: {e}")
            huffman_bits = 0
            huff_ratio = 0.0
        huffman_ratios.append(huff_ratio)
        
        # Test LZW compression
        try:
            lzw_codes = LZW.encode(text)
            lzw_bits = LZW.get_size_bits(lzw_codes)
            lzw_ratio = original_bits / lzw_bits if lzw_bits > 0 else 0.0
        except Exception as e:
            print(f"Error in LZW compression: {e}")
            lzw_bits = 0
            lzw_ratio = 0.0
        lzw_ratios.append(lzw_ratio)
        
        print(f"{filename:<20} | {actual_size:<15,} | {original_bits:<12} | {huffman_bits:<12} | {huff_ratio:<12.2f} | {lzw_bits:<12} | {lzw_ratio:<12.2f}")
        
        # Cleanup
        if os.path.exists(huff_output):
            os.remove(huff_output)
    
    print("-" * 100)
    
    # Print analysis
    print("\nCompression Rate Analysis (Wikipedia files):")
    if len(huffman_ratios) >= 2:
        size_ratio = file_sizes[-1] / file_sizes[0] if file_sizes[0] > 0 else 0
        print(f"  - Size increased by {size_ratio:.1f}x ({file_sizes[0]:,} -> {file_sizes[-1]:,} characters)")
        if huffman_ratios[0] > 0:
            print(f"  - Huffman compression ratio: {huffman_ratios[0]:.2f}x -> {huffman_ratios[-1]:.2f}x")
        if lzw_ratios[0] > 0:
            print(f"  - LZW compression ratio: {lzw_ratios[0]:.2f}x -> {lzw_ratios[-1]:.2f}x")
    
    print("\nWikipedia files compression rate analysis complete.")

if __name__ == '__main__':
    # Run compression ratio comparison tests
    run_tests()
    
    # Run time complexity analysis for random data
    print("\n" + "=" * 140)
    test_time_complexity()
    
    # Run time complexity analysis for Wikipedia files
    print("\n" + "=" * 140)
    test_wikipedia_time_complexity()