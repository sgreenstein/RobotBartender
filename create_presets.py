import urllib2
import urllib
import time
import os
import sys
import ingredient
import drink
import stt_google
import pyaudio
import wave
import pygame

def speak(text='hello', lang='en', fname='result_'+str(int(time.time()))+'.mp3', player='mplayer'):
    """ Send text to Google's text to speech service
    and returns created speech (wav file).
    Written by Jeyson Molina 8/30/2012
    Accessed on GitHub: https://github.com/jeysonmc/python-google-speech-scripts
    """
    limit = min(100, len(text))#100 characters is the current limit.
    text = text[0:limit]
    print "Text to speech:", text
    url = "http://translate.google.com/translate_tts"
    values = urllib.urlencode({"q": text, "textlen": len(text), "tl": lang})
    hrs = {"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7"}
    #TODO catch exceptions

    req = urllib2.Request(url, data=values, headers=hrs)
    p = urllib2.urlopen(req)
    f = open(fname, 'wb')
    f.write(p.read())
    f.close()

    print "Speech saved to:", fname
    pygame.mixer.init(16000)
    pygame.mixer.music.load(fname)
    pygame.mixer.music.play()
    while (pygame.mixer.music.get_busy()):
        z=1
    pygame.mixer.quit()
    os.remove(fname)

def main():
    Ingredient = ingredient.Ingredient
    Drink = drink.Drink
    stt = stt_google

    #Create preset ingredients
    #Alcoholic ingredients
    Rum = Ingredient("Rum", {"sweetness":.2, "proof":80, "flavorStrength":.3})
    Gin = Ingredient("Gin", {"proof":100, "flavorStrength":1})
    Whiskey = Ingredient("Whiskey", {"proof":86, "flavorStrength":0.5})
    Bourbon = Ingredient("Bourbon", {"proof":86, "flavorStrength":0.5})
    Scotch = Ingredient("Scotch", {"proof":86, "flavorStrength":0.5})
    Vodka = Ingredient("Vodka", {"proof":80})
    Tequila = Ingredient("Tequila", {"proof":80, "flavorStrength":0.7})
    Bitters = Ingredient("Bitters", {"proof":70, "bitterness":.5, "flavorStrength":0.9})
    Pisco = Ingredient("Pisco", {"proof":70, "sweetness":.2, "flavorStrength":0.5})

    #Liqueurs
    Kahlua = Ingredient("Kahlua", {"proof":40, "sweetness":.5, "flavorStrength":.5, "creaminess":1})
    IrishCream = Ingredient("Irish cream", {"proof":34, "sweetness":.3, "flavorStrength":.5, "creaminess":1})
    OrangeLiqueur = Ingredient("Orange liqueur", {"proof":62, "sweetness":.7, "flavorStrength":.6})
    PeppermintSchnapps = Ingredient("Peppermint schnapps", {"proof":50, "sweetness":.7, "flavorStrength":.7})
    BlueCuracao = Ingredient("Blue curacao", {"proof":48, "sweetness":.8, "flavorStrength":.6})

    #Nonalcoholic ingredients
    Milk = Ingredient("Milk", {"flavorStrength":.3, "creaminess":1})
    Coke = Ingredient("Coke", {"sweetness":.6, "flavorStrength":0.5, "carbonation":1})
    ClubSoda = Ingredient("Club soda", {"carbonation":1})
    LemonJuice = Ingredient("Lemon juice", {"sweetness":.3, "sourness":1, "flavorStrength":.7})
    LimeJuice = Ingredient("Lime juice", {"sweetness":.3, "sourness":1, "flavorStrength":.7})
    Grenadine = Ingredient("Grenadine", {"sweetness":1, "flavorStrength":.5})
    SimpleSyrup = Ingredient("Simple syrup", {"sweetness":1})
    GingerAle = Ingredient("Ginger ale", {"sweetness":.5, "flavorStrength":.3, "carbonation":1})
    OrangeJuice = Ingredient("Orange juice", {"sweetness":.2, "sourness ": 0.2, "flavorStrength":.5})
    Water = Ingredient("Water")

    #Create preset drinks
    RumAndCoke = Drink("Rum and Coke", {Rum:1,Coke:2})
    GinAndTonic = Drink("Gin and Tonic", {Gin:2,ClubSoda:5})
    WhiteRussian = Drink("White Russian", {Vodka:2,Milk:4,Kahlua:1})
    Piscola = Drink("Piscola", {Pisco:1,Coke:2})
    ShirleyTemple = Drink("Shirley Temple", {GingerAle:16,Grenadine:1})
    Margarita = Drink("Margarita", {OrangeLiqueur:1,Tequila:4,LemonJuice:1,LimeJuice:1,SimpleSyrup:2})
    Mojito = Drink("Mojito", {Rum:3,LimeJuice:1,SimpleSyrup:1,ClubSoda:5}) #mint
    MintJulep = Drink("Mint Julep", {Bourbon:4,SimpleSyrup:1}) #mint
    Screwdriver = Drink("Screwdriver", {Vodka:1,OrangeJuice:2})
    WhiskeySour = Drink("Whiskey Sour", {Whiskey:4,SimpleSyrup:3,LemonJuice:3})
    ElectricLemonade = Drink("Electrice Lemonade", {Rum:3,BlueCuracao:1,SimpleSyrup:3,LemonJuice:3})
    OldFashioned = Drink("Old-fashioned", {Whiskey:4,SimpleSyrup:2,Bitters:1})
    TequilaSunrise = Drink("Tequila Sunrise", {Tequila:8,OrangeJuice:12,Grenadine:1})
    MindEraser = Drink("Mind Eraser", {Vodka:1,Kahlua:1,ClubSoda:3})
    LongIslandIcedTea = Drink("Long Island Iced Tea", {Vodka:1,Gin:1,Rum:1,OrangeLiqueur:1,Tequila:1,SimpleSyrup:2,LemonJuice:2,Coke:1})
    RoyRogers = Drink("Roy Rogers", {Coke:9,Grenadine:1})
    speech = stt.listen_for_speech()
    if (speech):
        speak("Making a " + speech[0]["utterance"])

if __name__ == "__main__":
    main()
