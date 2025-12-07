def enc(text, key = 13):
    result = ""

    for c in text:
        if c.isalpha():
            start = ord('A') if c.isupper() else ord('a')
            addstart = ord(c) - start
            optkey = (addstart + key) % 26
            shift = chr(optkey + start)

            result += shift 
        else: 
            result += c
    return result

def bluh():

    tex = "hello"

    new_tex = enc(tex)

    print(new_tex)

bluh()