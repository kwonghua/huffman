import random
import string
import os

def create_random_text(filename="random.txt", size=10000):
    """
    Generates a file with a large body of text where character frequencies 
    are expected to be nearly uniform.
    """
    # Use a broad set of characters to ensure low frequency for any single one
    chars = string.ascii_letters + string.digits + ' ' + string.punctuation
    
    # Generate the text by randomly picking from the character set
    random_text = ''.join(random.choice(chars) for _ in range(size))
    
    # Save the file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(random_text)
        
    print(f"Generated {size} random characters in {filename}.")

if __name__ == '__main__':
    create_random_text()
    
    # Run this once, then you can delete the script and run test.py