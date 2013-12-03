#-------------------------------------------------------------------------------
# Name:        tts
# Purpose:
#
# Author:      Seth Greenstein, based on code from Jeyson Molina
#
# Created:     02/12/2013
# Copyright:   (c) someone 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def speak(text='hello', lang='en', fname='result.mp3'):
    """Send text to Google's text to speech service, plays result
    and returns created speech (wav file).

    Keyword arguments:
    text -- string of the text to say
    lang -- language (default en)
    fname -- filename of resulting sound (default result.mp3)

    Written by Jeyson Molina 8/30/2012
    Accessed on GitHub: https://github.com/jeysonmc/python-google-speech-scripts
    Altered by Seth Greenstein
    """
    #set up url parameters
    limit = min(100, len(text))#100 characters is the current limit.
    text = text[0:limit]
    print "Text to speech:", text
    url = "http://translate.google.com/translate_tts"
    values = urllib.urlencode({"q": text, "textlen": len(text), "tl": lang})
    hrs = {"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7"}
    #send to google, get result
    req = urllib2.Request(url, data=values, headers=hrs)
    p = urllib2.urlopen(req)
    with open(fname, 'wb') as f:
        f.write(p.read())
##    print "Speech saved to:", fname
    #play sound
    with open(fname, 'rb') as f:
        pygame.mixer.init(16000)
        pygame.mixer.music.load(f)
        pygame.mixer.music.play()
        #wait for sound to finish playing
        while (pygame.mixer.music.get_busy()):
            pass