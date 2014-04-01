import re

def include_all(result):
    return True

def url(result):
    """ return True if status has an url in text """
    return result.entities.get(u'urls')

def no_url(result):
    """ not(url) """
    return not(url(result))

def rt(result):
    """ return True if status is a RT """
    #Works only on real retweets (no replies with RT chain)
    return result.retweeted

def no_rt(result):
    """ not(rt )"""
    return not(rt(result))

def picture(result):
    """ return True if status has a picture """
    media =  result.entities.get('media')
    if media:
        return media[0].get('type') == u'photo'
    return False

def no_picture(result):
    """ not(pinture) """
    return not(picture(result))

def mention(result):
    """ search @ char for user mentions """
    return result.text.find('@')!=-1 and True or False

def no_mention(result):
    """ not(mention) """
    return not(mention(result))

def definition(result):
    """ return True if status text matched XXXX: pattern"""
    return  result.text.find(':') != -1 and True or False

def brackets(result):
    """ True if bracket count in text is 2"""
    return  len(re.findall(r'"', result.text)) == 2
    
