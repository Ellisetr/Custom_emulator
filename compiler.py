import re
import lang


def compile(text):
    input_text = text.split("\n")
    try:
        if not lexer(input_text):
            raise Exception
    except Exception:
        print("ERROR")
    return new_to_bin(input_text)


def lexer(text):
    for string in text:
        found = False
        for reg in lang.reg_list:
            if re.fullmatch(reg, string):
                found = True
        if not found:
            return False
    return True


def new_to_bin(text):
    bin_app = []
    for string in text:
        if re.fullmatch("^$| *|^((\/\/)(.*))", string):
            bin_app.append('0000000000000000')
        else:
            string = string.upper().split(" ")
            if string[0] == 'PUSH':
                bin_app.append(lang.com_code_list[string[0]] + format(int(string[1]), 'b').zfill(8))
            else:
                bin_app.append(lang.com_code_list[string[0]] + '0' * 8)
    print(bin_app)
    if bin_app[-1] != '1111111100000000':
        raise Exception
    return bin_app
