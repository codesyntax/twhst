import re

def _splitter(text, delimiter):
    splitted = text.split(delimiter)
    first = splitted[0]
    second = ' '.join(splitted[1:])
    return first, second
    
def first_whitespace(status):
    return _splitter(status.text, u' ')

def first_colon(status):
    return _splitter(status.text, u':')

def first_if_morethan_four(status):
    splitted = status.text.split()
    if len(splitted[0]) >= 4:
        first = splitted[0]
        second = ' '.join(splitted[1:])
    else:
        first = ' '.join(splitted[0:2])
        second = ' '.join(splitted[2:])
    return first, second

def between_brackets(status):
    match = re.match(r'"(.*?)"(.*)', status.text)
    if match:
        groups = match.groups()
        return groups[0], groups[1]
    else:
        #DBko zaharrak tratatzeko
        return _splitter(status.text, ' ')

