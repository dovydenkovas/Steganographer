"""
Steganography-Cipher-Program.py include functions:
- loading files who include algorithm ciphers (from ./data/ciphers).
- cipher text and write it in image.
- read ciphered text from image and uncipher it.
and run graphical interface from ./data.python.gui.
"""
from os import getcwd
from os import listdir
from os import system
import platform
import sys
from importlib import import_module as module

import cv2

import data.python.gui as gui
import data.python.u2b as u2b


def load_ciphers():
    """Load cipher files from data/ciphers
        and return list of loaded modules."""
    files = listdir(getcwd() + "/data/ciphers")
    return [module("data.ciphers." + filename[:-3]) for filename in files if '.py' in filename]


def write_image(infile, outfile, text, key, cipher_type, ciphers, show_info):
    """
    get infile - filename of source image.
        outfile - filename of image with steganographed and ciphered image.
        text - text of message.
        key - key world for ciphered text.
        cipher_type - what cipher algorithm use.
        ciphers - list of modules with cipher algorithms.
        ShowInfo - statusbar widget.
    cipher text and write it in image.
    """
    # cipher text
    for cipher in ciphers:
        if cipher.name == cipher_type:
            text = cipher.cipher(key, text) + cipher.cipher(key, chr(0) * 4)  # ciphered text + ciphered stop symbols
            break
    # translate text from string to list of bytes
    text = u2b.unicode2bit(text)

    # There are error with reading image from other drives in Windows.
    if platform.system() == "Windows":
        system('copy "' + infile.replace('/', '\\') + '" "' + getcwd() + '\\data\\last.png"')
        infile = "data\\last.png"

    image = cv2.imread(infile)
    # Write ciphered text to image
    for y in range(len(image)):
        for x in range(len(image[0])):
            for z in range(3):  # [R, G, B]
                if image[y, x][z] % 2 != 0: # if color is  additional
                    image[y, x][z] -= 1
                if len(text) > 0:
                    image[y, x][z] += text.pop(0)
                else:
                    break
            if len(text) == 0: break
        if len(text) == 0: break
        show_info(f"Запись {(100 * y * len(image[y]) * 3) // (16 * len(text))}%")

    if len(text) > 0:
        show_info("Изображение слишком маленькое для такого большого текста")
    else:
        # There are error with reading image from other drives in Windows.
        if platform.system() == "Windows":
            cv2.imwrite("data\\result.png", image)
            system(f"copy {getcwd()}\\data\\result.png " + outfile.replace('/', '\\'))
        else:
            cv2.imwrite(outfile, image)

        show_info('Операция завершена')


def read_image(infile, key, cipher_type, ciphers, show_info, win):
    """
    get infile - filename of image with steganographed and ciphered image.
        key - key world for ciphered text.
        cipher_type - what cipher algorithm use.
        ciphers - list of modules with cipher algorithms.
        ShowInfo - statusbar widget.
    cipher text and write it in image.
    """
    # What stop symbols?
    for cipher in ciphers:
        if cipher.name == cipher_type:
            stop = cipher.cipher(key, chr(0) * 4)

    # There are error with reading image from other drives in Windows.
    if platform.system() == "Windows":
        system('copy "' + infile.replace('/', '\\') + '" "' + getcwd() + '\\data\\last.png"')
        infile = "data\\last.png"

    image = cv2.imread(infile)  # source image
    bytes_text = []  # bytes of message
    text = ''  # text of message (translate from bytes)
    for x in range(len(image)):
        for y in range(len(image[0])):
            for z in range(3):  # [R, G, B]
                if image[x, y][z] % 2:  # if color is additional: 1
                    bytes_text += [1]
                else:  # if color is base: 0
                    bytes_text += [0]
                # check if end of the message (stop symbols)
                if not (y + x + z) % 512:  # every 32 symbols
                    text = u2b.bit2unicode(bytes_text)
                    if stop in text: break  # End reading image
            if stop in text: break
        if stop in text: break
        show_info(f"Прочитано {len(text)} символов")

    text = u2b.bit2unicode(bytes_text)
    if stop in text:
        # decipher text
        for cipher in ciphers:
            if cipher.name == cipher_type:
                text = text.split(stop)[0]  # select text before stop symbols
                win.message = cipher.uncipher(key, text[:-1]+text[len(text)-1])
                show_info('Операция завершена')
                return
    else:
        show_info("В изображении нет неявных сообщений")


if __name__ == '__main__':
    app = gui.QApplication(sys.argv)
    ex = gui.MainWindow(read_image, write_image, load_ciphers())
    sys.exit(app.exec_())
