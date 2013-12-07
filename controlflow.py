#-------------------------------------------------------------------------------
# Name:        controlflow
# Purpose:     receives commands and  acts on them appropriately
#
# Author:      Seth Greenstein
#
# Created:     02/12/2013
# Copyright:   (c) Seth Greenstein 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import stt_google
import tts
import similar_words
import create_presets
from heapq import nlargest
from random import choice
from novel_drink import NovelDrink

class ControlFlowHandler:
    """Handles the overall control flow of the robot
    """
    def __init__(self):
        """Returns a new control handler object
        """
        self._listen = stt_google.listen_for_speech
        self._speak = tts.speak
        self._commandsim = similar_words.SimilarWords('command_training.csv')
        self._flavorsim = similar_words.SimilarWords('flavor_training.csv')
        self._drinksim = similar_words.SimilarWords('drink_training.csv', penalty=10)
        self._amountsim = similar_words.SimilarWords('amount_training.csv')
        self._yesnosim = similar_words.SimilarWords('yesno_training.csv')
        self._drinks = create_presets.getdrinks()
        self._novel_drinks = NovelDrink()

    def handle(self):
        """Handles the overall control flow of the robot
        """
        speak = self._speak
        listen = self._listen
        drinks = self._drinks
##        drinks = dict(drinks, _load_novel_drinks())
        lastdrink = '' #for altering the most recently-made drink

        #keep receiving and processing commands until terminated
        while(True):
            try:
##                raw_input("Press enter to talk")
                spoken = raw_input("Enter what you would have said:")
            except KeyboardInterrupt:
                return
##            speech = listen()
            speech = [{'utterance': spoken}] #for testing without microphone
            if(not speech):
                #no input
                speak("I didn't hear you.")
                continue
            shouldconfirm = [False, False, False, False] #true if unsure
            #recognize speech
            command, shouldconfirm[0] = self._commandsim.classify(speech)
            drink, shouldconfirm[1] = self._drinksim.classify(speech, threshold = 0.4)
            flavor, shouldconfirm[2] = self._flavorsim.classify(speech)
            amount, shouldconfirm[3] = self._amountsim.classify(speech)

            #perform checks
            print "Command:", command, "Drink:", drink, "Flavor:", flavor, "Amount:", amount
            if(not command):
                #there must be a command
                speak("I didn't understand that.")
                continue
            if(True in shouldconfirm):
##            if(True in shouldconfirm or not drink):
                #user said no to confirmation
                if(self._confirm(command, flavor, amount, drink, lastdrink)):
                    print "Confirmed."
                else:
                    continue

            #act based on recognized speech
            if(command=='alter'):
                if(not drink):
                    #no drink specified. They probably meant the last drink,
                    #unless there was no last drink
                    if(not lastdrink):
                        speak("I don't know to which drink you are referring.")
                        continue
                    drink = lastdrink
                if(flavor == 'good'):
                    drinks[drink].wasgood()
                    speak("I'm glad you liked the " + drink)
                elif(flavor == 'bad'):
                    drinks[drink].wasbad()
                    speak("I'm sorry you didn't like the " + drink)
                    if drinks[drink].hasfailed():
                        speak("Never again will I make a " + drink)
                        drinks.pop(drink)
                else:
                    if(not amount or not flavor):
                        #we need an amount to be able to alter the flavor
                        speak("I didn't understand that.")
                        continue
                    drinks[drink].alter_recipe(flavor, float(amount))
            else: #command must be 'make'
                if(drink):
                    #a drink is specified. make that drink
                    drinks[drink].make(flavor)
                    lastdrink = drink
                else:
                    if(flavor):
                        randomdrink = self._randomdrink(flavor)
                        randomdrink.make()
                        lastdrink = randomdrink
                    else:
                        #no drink or flavor specified. Make something new!
                        print "Making new drink:"
                        self._novel_drinks.makenovel() #TODO: change this method call
##                        drinks[newdrink.name] = newdrink
##                        newdrink.make()
##                        lastdrink = newdrink.name

    def _confirm(self, command, flavor, amount, drink, lastdrink):
        """Asks the user to confirm a guessed action

        Keyword arguments:
        command -- 'make' or 'alter'
        flavor -- e.g. 'sour' or 'sweet' or 'bad'
        amount -- 0.1 or -0.1
        drink -- e.g. 'Rum and Coke'
        """
        speak = self._speak
        listen = self._listen
        assert command #no point in confirming if there is no command
        if(command == 'make'):
            if(not drink):
                drink = 'drink'
                if(not flavor):
                    flavor = 'new'
                elif (flavor == 'alcoholic'):
                    flavor = 'strong'
            speak("Do you want me to make you a " + flavor + ' ' + drink + "?")
        else:
            if(not drink):
                drink = lastdrink
            if(flavor == 'bad' or flavor == 'good'):
                speak("Did you say that the " + drink + " was " + flavor + "?")
            else:
                if(float(amount) > 0):
                    change = 'more'
                else:
                    change = 'less'
                speak("Do you want to make the " + drink + ' ' + change + ' ' + flavor + "?")

        #listen for yes or no
        confirmation = ''
        while(confirmation == ''):
            speech = listen()
            while(not speech):
                speak("I didn't hear you.")
                speech = listen()
            confirmation, _ = self._yesnosim.classify(speech, threshold = 0.05)
            if(confirmation == ''):
                speak("I didn't understand that")
        if(confirmation == 'yes'):
            return True
        else:
            return False

    def _randomdrink(self, flavor = 'none'):
        """returns a random drink from drinks that is in the upper quartile
        of the specified flavor

        Keyword arguments:
        flavor -- flavor to make sure the drink has, e.g. 'sweet' (default none)
        """
        drinks = self._drinks
        if(flavor == 'none'):
            return choice(drinks.keys())
        #find top few drinks using heap
        top = nlargest(len(drinks) / 5, drinks, key = lambda k: drinks[k].level_of(flavor))
        for index, drink in enumerate(top):
            print index + 1, drinks[drink].name, '\t%.2f' % drinks[drink].level_of(flavor)
        #return a random drink from the top few
        selected_drink = drinks[choice(top)]
        #drink must have at least some of the specified flavor
        while(selected_drink.level_of(flavor) == 0):
            selected_drink = drinks[choice(top)]
        return selected_drink

    def _load_novel_drinks(self):
        """loads the drinks that were previously created by conceptual blending
        and saved to a file
        """
        pass
        #TODO: open the novel drinks file, read it, return dictionary with
        #keys drink names and values Drink objects

def main():
    cfh = ControlFlowHandler()
    cfh.handle()

if __name__ == '__main__':
    main()