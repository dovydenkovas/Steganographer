from os import getcwd
from os import listdir
from os import system
import platform
import sys
from importlib import import_module as module

import cv2

import data.python.gui as gui
import data.python.u2b as u2b



ciphers = []
def LoadCiphers():
    '''Load cipher files from data\ciphers'''
    global ciphers
    files = listdir(getcwd()+"/data/ciphers")
    ciphers_ = []
    for f in files:
        if '.py' in f:
            ciphers_ += ["data.ciphers."+f[:-3]]
    for i in ciphers_:
        cipher = module(i)
        ciphers += [cipher]


def Write(input, output, text, key, type, ShowInfo):  # Запись сообщения в файл
    for ciph in ciphers:
        if ciph.name == type:
            text = ciph.cipher(key, text)
            text += ciph.cipher(key, chr(0) * 4)
    text = u2b.unicode2bite(text)

    # В Windows есть проблемы с чтением полных путей с помощью imread:
    if platform.system() == "Windows":
        system('copy "' + input.replace('/', '\\') + '" "' + getcwd() + '\\data\\last.png"')
        input = "data\\last.png"

    img = cv2.imread(input)
    # Изменяем изображение
    for x in range(len(img)):
        for y in range(len(img[0])):
            # Все дополнительные цвета делаем базовыми
            for i in range(3):
                if img[x, y][i] % 2 != 0:
                    img[x, y][i] -= 1
                if len(text) > 0:
                    img[x, y][i] += text.pop(0)
                else:
                    break
            if len(text) == 0: break
        if len(text) == 0: break
        ShowInfo(f"Запись {(100 * i) // (len(text))}%")

    if len(text) > 0:
        ShowInfo("Изображение слишком маленькое для такого большого текста")
    else:
        # В Windows есть проблемы с чтением полных путей с помощью imwrite поэтому костыль:
        if platform.system() == "Windows":
            cv2.imwrite("data\\result.png", img)
            system(f"copy {getcwd()}\\data\\result.png " + output.replace('/','\\'))
        else:
            cv2.imwrite(output, img)

        ShowInfo('Операция завершена')


def Read( input, key, type, ShowInfo, win):  # Чтение сообщения из файла
    for ciph in ciphers:
        if ciph.name == type:
            stop = ciph.cipher(key, chr(0) * 4)

    # В Windows есть проблемы с чтением полных путей с помощью imread поэтому костыль:
    if platform.system() == "Windows":
        system('copy "' + input.replace('/', '\\') + '" "' + getcwd() + '\\data\\last.png"')
        input = "data\\last.png"

    img = cv2.imread(input)
    text = ''
    bite = []
    # Читаем изображение
    for x in range(len(img)):
        for y in range(len(img[0])):
            for i in range(3):
                if img[x, y][i] % 2:  # Если цвет дополнительный - 1
                    bite += [1]
                else:  # Если базовый - 0
                    bite += [0]
                if not (y+x+i)%512: # Проверяем окончание сообщения каждые 32 символа
                    text = u2b.bite2unicode(bite)
                    if stop in text: break
            if stop in text: break
        if stop in text: break
        ShowInfo(f"Прочитано {len(text)} символов")

    text = u2b.bite2unicode(bite)
    if stop in text:
        for ciph in ciphers:
            if ciph.name == type:
                text = text.split(stop)[0]
                win.message = ciph.uncipher(key, text[:-1]) #-4
                ShowInfo('Операция завершена')
                break
    else:
        ShowInfo("В изображении нет неявных сообщений")



if __name__ == '__main__':
    LoadCiphers()
    app = gui.QApplication(sys.argv)
    ex = gui.MainWindow(Read,Write,ciphers)
    sys.exit(app.exec_())
