""" Translate unicode string or byte string to list of bits

 unicode2bit(string)  - function to translate unicode string or bite string to bit list;
 bit2unicode(bytes_list) -  function to translate bit list to unicode string.

"""


def unicode2bit(unicode_list):
    """ Convert string or byte string to list of bits by unicode table """
    if type(unicode_list) == bytes:
        unicode_list = unicode_list.decode()
    bits_of_message = []
    # for char_number in list of codes of symbols of string
    for char_number in [ord(symbol) for symbol in unicode_list]:
        # convert decimal number to binary number (list of bits)
        bits_of_symbol = [int(bit) for bit in list(bin(char_number)[2:])]
        # add fist zeros to 16 bit
        while len(bits_of_symbol) < 16:
            bits_of_symbol = [0] + bits_of_symbol
        bits_of_message += bits_of_symbol
    return bits_of_message


def bit2unicode(bits: list):
    """ Convert list of bites in string by unicode table"""
    string = ""
    b = 0
    while b + 16 <= len(bits):
        s = 0
        for i in range(b, b + 16):
            s += int(bits[i]) * 2 ** (16 - (i - b))
        b += 16
        string += chr(s // 2)
    return string


