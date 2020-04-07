""" Module consist of cipher and decipher function to (de)ciphering messages with Caesar cipher """
name = "Шифр Цезаря"

def cipher(key,string):
    keys = [ord(key[0])]
    k = 0
    code = [ord(i) for i in string]
    for i in range(0, len(code)):
        code[i] += keys[k]
        if code[i] >= 65536:
            code[i] -= 65536
        if k+1 < len(keys):
            k += 1
        else:
            k = 0
    return ''.join([chr(i) for i in code])

def uncipher(key,string):
    keys = [ord(key[0])]
    k = 0
    code = [ord(i) for i in string]
    for i in range(0, len(code)):
        code[i] -= keys[k]
        if code[i] < 0:
            code[i] += 65536
        if k+1 < len(keys):
            k += 1
        else:
            k = 0
    return ''.join([chr(i) for i in code])
