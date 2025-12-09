import heapq
import os
from collections import Counter
import json
import ast # Used for safely reading the frequency dict back from file

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        """Allows heapq to compare nodes based on frequency."""
        return self.freq < other.freq

# --- 1. Tree Construction ---

def build_huffman_tree(text):
    """Builds the Huffman Tree based on character frequencies."""
    if not text:
        return None, {}
        
    frequency = Counter(text)
    # Create nodes and push them onto the min-heap
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)
    
    # Combine the two lowest-frequency nodes until only one remains (the root)
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        
        # Create a new internal node
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)
    
    return heap[0], frequency

def build_codes(node, prefix="", codebook=None):
    """Recursively generates the Huffman codes (codebook) from the tree."""
    if codebook is None:
        codebook = {}
        
    if node:
        if node.char is not None: # Leaf node (contains a character)
            codebook[node.char] = prefix
        build_codes(node.left, prefix + "0", codebook)
        build_codes(node.right, prefix + "1", codebook)
    return codebook

# --- 2. Compression ---

def compress_to_file(text, output_filename):
    """Compresses the given text using Huffman coding and writes to a file."""
    if not text:
        print("Input text is empty.")
        return 0
        
    # 1. Build Tree & Codes
    root, frequency = build_huffman_tree(text)
    codes = build_codes(root)
    
    # Handle single character input (a necessary edge case)
    if len(frequency) == 1:
        char = list(frequency.keys())[0]
        codes[char] = "0"

    # 2. Encode Data
    encoded_bits = "".join(codes[char] for char in text)
    
    # 3. Padding bits to make it a full byte
    padding = 8 - (len(encoded_bits) % 8)
    if padding == 8:
        padding = 0
    
    encoded_bits += "0" * padding
    
    # Convert bit string to actual bytes
    byte_array = bytearray()
    for i in range(0, len(encoded_bits), 8):
        byte = encoded_bits[i:i+8]
        byte_array.append(int(byte, 2))
    
    # 4. Write to File (Header + Data)
    # Write in binary mode ('wb') to store actual bytes
    with open(output_filename, 'wb') as f:
        # Header: Write frequency table (as a JSON string for easy parsing)
        f.write(json.dumps(frequency).encode('utf-8') + b'\n') 
        # Header: Write padding size
        f.write(str(padding).encode('utf-8') + b'\n')
        # Data: Write the compressed bytes
        f.write(byte_array) 
        
    # Calculate total data bits written for the caller
    total_encoded_bits_written = len(byte_array) * 8
    print(f"Compressed {len(text)} chars to {total_encoded_bits_written} bits in {output_filename}.")
    return total_encoded_bits_written

# --- 3. Decompression ---

def build_tree_from_frequency(frequency):
    """Rebuilds the Huffman Tree from the frequency map read from the header."""
    if not frequency:
        return None
        
    # Identical to the start of build_huffman_tree but uses the given frequency map
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)
        
    # Handle single character edge case
    if not heap:
        return HuffmanNode(None, 0) # Empty tree
    
    return heap[0]

def decompress_from_file(input_filename):
    """Decompresses the contents of the given file."""
    # Read in binary mode ('rb')
    with open(input_filename, 'rb') as f:
        # 1. Read Header (Frequency Table and Padding)
        
        # Read the first line (frequency map)
        frequency_line = f.readline().strip()
        # Read the second line (padding)
        padding_line = f.readline().strip()
        
        # Decode and parse the header data
        try:
            frequency = json.loads(frequency_line.decode('utf-8'))
            padding = int(padding_line.decode('utf-8'))
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error reading file header: {e}")
            return ""

        # 2. Rebuild Tree
        root = build_tree_from_frequency(frequency)
        if not root or not frequency:
            return ""
        
        # 3. Read Data
        compressed_data = f.read()
        
    # Convert bytes back to a bit string
    bit_string = ""
    for byte in compressed_data:
        # Convert byte to 8-bit binary string (e.g., 5 -> '00000101')
        bit_string += bin(byte)[2:].zfill(8)
        
    # Remove padding bits from the end
    if padding > 0:
        bit_string = bit_string[:-padding]
        
    # 4. Decode Data
    decoded_text = []
    current_node = root
    
    # Single character edge case: if only one char, the code is "0"
    if len(frequency) == 1:
        # Simply repeat the character by the total frequency count
        char = list(frequency.keys())[0]
        return char * frequency[char]

    for bit in bit_string:
        if bit == '0':
            current_node = current_node.left
        else: # bit == '1'
            current_node = current_node.right
            
        if current_node.char is not None: # Reached a leaf node
            decoded_text.append(current_node.char)
            current_node = root # Reset to the root for the next character
            
    return "".join(decoded_text)