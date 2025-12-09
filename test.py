import time
import math
import os
import huffman 

# --- Comparison Algorithm: Run-Length Encoding ---

def rle_encode(text):
    """Simple Run-Length Encoding (RLE) for comparison."""
    if not text: 
        return ""
    
    encoded = []
    count = 1
    
    # Iterate through the text to find runs
    for i in range(1, len(text)):
        if text[i] == text[i-1]:
            count += 1
        else:
            # Append the character and its count
            encoded.append(text[i-1] + str(count))
            count = 1
            
    # Append the final run
    encoded.append(text[-1] + str(count))
    return "".join(encoded)

# --- Main Test Execution ---

def run_tests():
    """Runs tests on different file types and compares compression ratios."""
    # NOTE: Ensure these files (wikipedia.txt, random.txt, etc.) exist in the same directory!
    files = ["wikipedia.txt", "random.txt", "equal_dist.txt", "single_char.txt"]
    
    # Create a simple file for testing the single-character edge case
    with open("single_char.txt", 'w') as f:
        f.write("A" * 500)
    
    print("\n" + "=" * 115)
    print("✨ Huffman Coding vs. RLE Compression Test Suite (with Ratios) ✨")
    print("=" * 115)
    
    # Print table header - ADDING RATIO COLUMNS
    print(
        f"{'File':<18} | {'Original (Bits)':<15} | "
        f"{'Huffman (Bits)':<15} | {'Huffman Ratio':<15} | "
        f"{'RLE (Bits)':<15} | {'RLE Ratio':<15} | "
        f"{'Integrity Check':<15}"
    )
    print("-" * 115)
    
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
        
        # --- 2. Run Huffman Compression and Decompression ---
        huff_output_file = "temp_huffman.bin"
        
        try:
            huffman_data_bits = huffman.compress_to_file(original_text, huff_output_file)
        except Exception as e:
            print(f"Error during Huffman compression for {filename}: {e}")
            huffman_data_bits = 0
            huffman_decompressed = ""

        # Calculate Huffman Ratio
        huff_ratio = original_bits / huffman_data_bits if huffman_data_bits > 0 else 0.0

        # Decompress and verify
        if huffman_data_bits > 0:
            huffman_decompressed = huffman.decompress_from_file(huff_output_file)
            is_intact = "PASS" if huffman_decompressed == original_text else "FAIL"
        else:
            is_intact = "N/A"
            
        # --- 3. Run RLE Comparison ---
        rle_res = rle_encode(original_text)
        rle_bits = len(rle_res.encode('utf-8')) * 8 
        
        # Calculate RLE Ratio
        rle_ratio = original_bits / rle_bits if rle_bits > 0 else 0.0
        
        # --- 4. Print Results ---
        print(
            f"{filename:<18} | "
            f"{original_bits:<15} | "
            f"{huffman_data_bits:<15} | "
            f"{huff_ratio:<15.2f} | " # Format ratio to 2 decimal places
            f"{rle_bits:<15} | "
            f"{rle_ratio:<15.2f} | " # Format ratio to 2 decimal places
            f"{is_intact:<15}"
        )

    print("-" * 115)
    
    # Cleanup temporary files
    if os.path.exists("temp_huffman.bin"):
        os.remove("temp_huffman.bin")
    if os.path.exists("single_char.txt"):
        os.remove("single_char.txt")
    print("\nCleanup complete.")

if __name__ == '__main__':
    run_tests()