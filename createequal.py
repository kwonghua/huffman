import os
import string # Import string for easy access to character sets

def create_equal_dist_text(filename="equal_dist.txt", pattern="AABBCCDD", total_size=10000):
    """
    Generates a file by repeating a pattern, testing both Huffman and RLE.
    
    Modified to use a larger pattern of unique characters to demonstrate 
    Huffman's poor performance when frequencies are uniform.
    """
    
    new_pattern = string.ascii_uppercase + string.digits[:6] # 26 + 6 = 32 unique chars
    
    pattern = new_pattern
    
    
    pattern_length = len(pattern)
    
    # Calculate how many times the pattern needs to be repeated
    repetitions = total_size // pattern_length
    
    # Create the repeating text
    repeating_text = (pattern * repetitions)
    
    # Add any remaining characters to reach the exact size (if needed)
    repeating_text += pattern[:total_size % pattern_length]
    
    # Save the file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(repeating_text)
        
    print(f"Generated {len(repeating_text)} characters in {filename} using pattern with {len(new_pattern)} unique chars.")

if __name__ == '__main__':
    # Run the function with the new, long pattern
    create_equal_dist_text(total_size=80000) # Increased size to better show data compression vs header size