def rot13(text):
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
    special = {'<' : '&lt;', '>' : '&gt;', '"': '&quot;', '&':'&amp;'}
    list = []
    for letter in text:
        if letter in lowercase:
            number = ord(letter)
            if number >= 110:
                number = 97 + number - 110
            else:
                number += 13
            list.append(chr(number))
        elif letter in uppercase:
            number = ord(letter)
            if number >= 78:
                number = 65 + number - 78
            else:
                number += 13
            list.append(chr(number))
        elif letter in special:
            list.append(special[letter])
        else:
            list.append(letter)
    return ''.join(list)