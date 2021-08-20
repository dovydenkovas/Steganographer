# This file is part of Steganographer project.
#
# Copyright 2021 The Steganographer contributors
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
    Translate unicode string or byte string to list of bits

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
