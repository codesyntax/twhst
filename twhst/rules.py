
def include_all(result):
    return True

def url(result):
    """ return True if status has an url in text """
    return result.entities.get(u'urls')

def no_url(result):
    return not(url(result))

def rt(result):
    """ return True if status is a RT """
    return result.retweeted

def no_rt(result):
    return not(rt(result))

def picture(result):
    """ return True if status has a picture """
    pass

def no_picture(result):
    return not(picture(result))

def definition(result):
    """ return True if status text matched XXXX: pattern"""
    return  result.text.find(':') != -1 and True or False

    
