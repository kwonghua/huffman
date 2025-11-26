import heapq
import os
from collections import Counter

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    frequency = Counter(text)
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)
    
    return heap[0], frequency

def build_codes(node, prefix="", codebook={}):
    if node:
        if node.char is not None:
            codebook[node.char] = prefix
        build_codes(node.left, prefix + "0", codebook)
        build_codes(node.right, prefix + "1", codebook)
    return codebook

def compress_to_file(text, output_filename):
    # 1. Build Tree & Codes
    root, frequency = build_huffman_tree(text)
    codes = build_codes(root)
    
    # 2. Encode Data
    encoded_bits = "".join(codes[char] for char in text)
    
    # DESIGN CHOICE: Padding bits to make it a full byte
    padding = 8 - (len(encoded_bits) % 8)
    encoded_bits += "0" * padding
    
    # 3. Write to File (Header + Data)
    with open(output_filename, 'w') as f:
        # Header: Write frequency table (Overhead!)
        f.write(str(frequency) + "\n") 
        f.write(str(padding) + "\n")
        f.write(encoded_bits) # In real life, write as bytes, but string is easier for students
        
    print(f"Compressed {len(text)} chars to {len(encoded_bits)} bits.")