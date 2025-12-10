"""
Standard ASCII Baseline:
Every character uses exactly 8 bits.
"""

class FixedLength:
    """
    Standard ASCII Baseline:
    Every character uses exactly 8 bits.
    """
    @staticmethod
    def get_size_in_bits(text):
        return len(text) * 8

