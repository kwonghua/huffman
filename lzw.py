"""
Lempel-Ziv-Welch (LZW) Compression
Full implementation: Encoding and Decoding.
"""

class LZW:
    """
    Lempel-Ziv-Welch (LZW) Compression
    Full implementation: Encoding and Decoding.
    """
    @staticmethod
    def encode(text):
        """Compresses a string into a list of output codes."""
        if not text: return []
        
        # Convert text to UTF-8 bytes to handle all Unicode characters properly
        text_bytes = text.encode('utf-8')
        
        # 1. Initialize dictionary with all possible byte values (0-255)
        dictionary = {bytes([i]): i for i in range(256)}
        dict_size = 256
        
        current_string = b""
        result_codes = []
        
        for byte in text_bytes:
            byte_seq = bytes([byte])
            combined = current_string + byte_seq
            
            if combined in dictionary:
                current_string = combined
            else:
                # Output the code for the prefix we found
                if current_string:
                    result_codes.append(dictionary[current_string])
                
                # Add the new combination to the dictionary
                dictionary[combined] = dict_size
                dict_size += 1
                
                current_string = byte_seq
        
        # Output the last string
        if current_string:
            result_codes.append(dictionary[current_string])
            
        return result_codes

    @staticmethod
    def decode(compressed_codes):
        """Decompresses a list of codes back into a string."""
        if not compressed_codes: return ""
        
        # 1. Initialize dictionary with all possible byte values (0-255)
        dictionary = {i: bytes([i]) for i in range(256)}
        dict_size = 256
        
        # 2. Read the first code
        old_code = compressed_codes[0]
        result_bytes = dictionary[old_code]
        current_byte = result_bytes[0:1]  # Get first byte as bytes object
        
        # 3. Loop through the rest
        for new_code in compressed_codes[1:]:
            if new_code in dictionary:
                entry = dictionary[new_code]
            elif new_code == dict_size:
                # Special case: cScSc pattern
                entry = dictionary[old_code] + current_byte
            else:
                raise ValueError(f"Bad compressed code: {new_code}")
            
            result_bytes += entry
            
            # Add new phrase to dictionary
            dictionary[dict_size] = dictionary[old_code] + entry[0:1]
            dict_size += 1
            
            old_code = new_code
            current_byte = entry[0:1]
        
        # Convert bytes back to UTF-8 string
        return result_bytes.decode('utf-8')

    @staticmethod
    def get_size_bits(compressed_codes):
        # Estimate: 12 bits per code
        return len(compressed_codes) * 12

