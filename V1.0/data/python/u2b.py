"""
 This module is consist of two functions:
 1) Function to translate unicode string to bit list;
 2) Function to translate bit list to unicode string.
"""


def unicode2bit(string: str):
    """Convert string to list of bits by unicode table"""
    bits = []
    for s in string:
        a = ord(s)
        b = []
        # convert dec number to bin
        while a > 0:
            b = [a % 2] + b
            a = a // 2
        # add fist zeros to 16 bit
        while len(b) < 16:
            b = [0] + b
        bits += b
    return bits


def bit2unicode(bits: list):
    """convert list of bites in string by unicode table"""
    string = ""
    b = 0
    while b + 16 <= len(bits):
        s = 0
        for i in range(b, b + 16):
            s += int(bits[i]) * 2 ** (16 - (i - b))
        b += 16
        string += chr(s // 2)
    return string
