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
import similar_words

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

def getdrinks():
    Ingredient = ingredient.Ingredient
    Drink = drink.Drink
    #Create preset ingredients
    #Alcoholic ingredients
    Rum = Ingredient("Rum", {"sweetness":.2, "alcohol":80, "flavor_strength":.3})
    Gin = Ingredient("Gin", {"alcohol":100, "flavor_strength":1})
    Whiskey = Ingredient("Whiskey", {"alcohol":86, "flavor_strength":0.5})
    Bourbon = Ingredient("Bourbon", {"alcohol":86, "flavor_strength":0.5})
    Scotch = Ingredient("Scotch", {"alcohol":86, "flavor_strength":0.5})
    Vodka = Ingredient("Vodka", {"alcohol":80})
    Tequila = Ingredient("Tequila", {"alcohol":80, "flavor_strength":0.7})
    Bitters = Ingredient("Bitters", {"alcohol":70, "bitterness":.5, "flavor_strength":0.9})
    Pisco = Ingredient("Pisco", {"alcohol":70, "sweetness":.2, "flavor_strength":0.5})

    #Liqueurs
    Kahlua = Ingredient("Kahlua", {"alcohol":40, "sweetness":.5, "flavor_strength":.5, "creaminess":1})
    IrishCream = Ingredient("Irish cream", {"alcohol":34, "sweetness":.3, "flavor_strength":.5, "creaminess":1})
    OrangeLiqueur = Ingredient("Orange liqueur", {"alcohol":62, "sweetness":.7, "flavor_strength":.6})
    PeppermintSchnapps = Ingredient("Peppermint schnapps", {"alcohol":50, "sweetness":.7, "flavor_strength":.7})
    BlueCuracao = Ingredient("Blue curacao", {"alcohol":48, "sweetness":.8, "flavor_strength":.6})

    #Nonalcoholic ingredients
    Milk = Ingredient("Milk", {"flavor_strength":.3, "creaminess":1})
    Coke = Ingredient("Coke", {"sweetness":.6, "flavor_strength":0.5, "carbonation":1})
    ClubSoda = Ingredient("Club soda", {"carbonation":1})
    LemonJuice = Ingredient("Lemon juice", {"sweetness":.3, "sourness":1, "flavor_strength":.7})
    LimeJuice = Ingredient("Lime juice", {"sweetness":.3, "sourness":1, "flavor_strength":.7})
    Grenadine = Ingredient("Grenadine", {"sweetness":1, "flavor_strength":.5})
    SimpleSyrup = Ingredient("Simple syrup", {"sweetness":1})
    GingerAle = Ingredient("Ginger ale", {"sweetness":.5, "flavor_strength":.3, "carbonation":1})
    OrangeJuice = Ingredient("Orange juice", {"sweetness":.2, "sourness": 0.2, "flavor_strength":.5})
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
    ElectricLemonade = Drink("Electric Lemonade", {Rum:3,BlueCuracao:1,SimpleSyrup:3,LemonJuice:3})
    OldFashioned = Drink("Old-fashioned", {Whiskey:4,SimpleSyrup:2,Bitters:1})
    TequilaSunrise = Drink("Tequila Sunrise", {Tequila:8,OrangeJuice:12,Grenadine:1})
    MindEraser = Drink("Mind Eraser", {Vodka:1,Kahlua:1,ClubSoda:3})
    LongIslandIcedTea = Drink("Long Island Iced Tea", {Vodka:1,Gin:1,Rum:1,OrangeLiqueur:1,Tequila:1,SimpleSyrup:2,LemonJuice:2,Coke:1})
    RoyRogers = Drink("Roy Rogers", {Coke:9,Grenadine:1})
    ScotchAndSoda = Drink("Scotch and Soda", {Scotch:2,ClubSoda:1})
    BourbonAndWater = Drink("Bourbon and Water", {Bourbon:2,Water:1})
    CubaLibre = Drink("Cuba Libre", {Rum:2,Coke:4,LimeJuice:1})
    PiscoSour = Drink("Pisco Sour", {Pisco:3,LemonJuice:2,LimeJuice:1,Water:2,SimpleSyrup:1})
    DarkAndStormy = Drink("Dark and Stormy", {Rum:2, GingerAle:3})
    GinBuck = Drink("Gin Buck", {Gin:2, GingerAle:3})
    GinRickey = Drink("Gin Rickey", {Gin:4, LimeJuice:1, ClubSoda:6})
    TomCollins = Drink("Tom Collins", {Gin:3,LemonJuice:2,SimpleSyrup:1,ClubSoda:4})
    MoscowMule = Drink("Moscow Mule", {Vodka:2,LimeJuice:1,GingerAle:2})
    VodkaTonic = Drink("Vodka Tonic", {Vodka:4,ClubSoda:6,LimeJuice:1})
    BlackRussian = Drink("Black Russian", {Vodka:7,Kahlua:3})

    #Create preset drink dictionary
    drinks = {RumAndCoke.name:RumAndCoke,
        GinAndTonic.name:GinAndTonic,
        WhiteRussian.name:WhiteRussian,
        Piscola.name:Piscola,
        ShirleyTemple.name:ShirleyTemple,
        Margarita.name:Margarita,
        Mojito.name:Mojito,
        MintJulep.name:MintJulep,
        Screwdriver.name:Screwdriver,
        WhiskeySour.name:WhiskeySour,
        ElectricLemonade.name:ElectricLemonade,
        OldFashioned.name:OldFashioned,
        TequilaSunrise.name:TequilaSunrise,
        MindEraser.name:MindEraser,
        LongIslandIcedTea.name:LongIslandIcedTea,
        RoyRogers.name:RoyRogers,
        ScotchAndSoda.name:ScotchAndSoda,
        BourbonAndWater.name:BourbonAndWater,
        CubaLibre.name:CubaLibre,
        PiscoSour.name:PiscoSour,
        DarkAndStormy.name:DarkAndStormy,
        GinBuck.name:GinBuck,
        GinRickey.name:GinRickey,
        TomCollins.name:TomCollins,
        MoscowMule.name:MoscowMule,
        VodkaTonic.name:VodkaTonic,
        BlackRussian.name:BlackRussian
        }
    return drinks

def main():
    Ingredient = ingredient.Ingredient
    stt = stt_google

    #get instruction
    drink_sim = similar_words.SimilarWords('drink_training_old.csv')
    drinks = getdrinks()
    speak("What drink should I make you?")
##    speech = stt.listen_for_speech()
    speech = [{'utterance':"make me a rum and coke"}]#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    print speech
    while(not speech):
        speak("I didn't hear you. What drink would you like?")
        speech = stt.listen_for_speech()
    drinkname = drink_sim.classify(speech)
    if(not drinkname in drinks):
        speak("I don't know how to make that.")
        return
    #make drink
    drinks[drinkname].make()
    speak("Your " + drinkname + " is ready.")
    time.sleep(2)
    #get feedback and alter recipe if necessary
    flavor_sim = similar_words.SimilarWords('flavor_training_old.csv')
    amount_sim = similar_words.SimilarWords('amount_training_old.csv', 1)
    speak("How was your " + drinkname + "?")
    speech = stt.listen_for_speech()
    print speech
    speech = stt.listen_for_speech()
    if(not speech):
        return
    flavor = flavor_sim.classify(speech, 0.08)
    if(flavor in Ingredient.flavorlist()):
        amount = amount_sim.classify(speech, 0)
        print "Flavor:", flavor
        print "Amount:", amount
        if drinks[drinkname].alter_recipe(flavor, float(amount)):
            if(float(amount) > 0):
                change = "more"
            else:
                change = "less"
##            if(abs(float(amount)) > 0.1):
##                change = "much " + change
            speak("Next time your " + drinkname + " will have " + change + " " + flavor)
        else:
            if(drinkname[0].lower() in ['a', 'e', 'i', 'o', 'u']):
                article = 'an'
            else:
                article = 'a'
            speak("Nothing in " + article + ' ' + drinkname + " has any " + flavor)
    elif(flavor == 'bad'):
        speak("I'm sorry you didn't like it.")
    elif(flavor == 'good'):
        speak("I'm glad you liked it!")
    else:
        #didn't match anything with sufficient confidence
        speak("I don't know what to do with that information.")

if __name__ == "__main__":
    main()
