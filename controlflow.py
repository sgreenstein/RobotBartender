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

class ControlFlowHandler:
    def __init__(self):
        self._listen = stt_google.listen_for_speech
        self._speak = tts.speak
        self._commandsim = similar_words.SimilarWords('command_training.csv')
        self._flavorsim = similar_words.SimilarWords('flavor_training.csv')
        self._drinksim = similar_words.SimilarWords('drink_training.csv')
        self._amountsim = similar_words.SimilarWords('amount_training.csv')
        self._yesnosim = similar_words.SimilarWords('yesno_training.csv')
        self._drinks = create_presets.getdrinks()

    def handle(self):
        speak = self._speak
        listen = self._listen
        drinks = self._drinks
##        drinks = dict(drinks, load_novel_drinks())
        lastDrink = ''
        while(True):
##            while(not buttonPress): #TODO: implement button pressing
##                pass
            try:
                raw_input("Press enter to talk")
            except KeyboardInterrupt:
                return
            speech = listen()
##            speech = [{'utterance': 'make me a rum and coke'}]
            if(not speech):
                speak("I didn't hear you.")
                continue
            shouldconfirm = [False, False, False, False]
            command, shouldconfirm[0] = self._commandsim.classify(speech)
            drink, shouldconfirm[1] = self._drinksim.classify(speech)
            flavor, shouldconfirm[2] = self._flavorsim.classify(speech)
            amount, shouldconfirm[3] = self._amountsim.classify(speech)
            if(not command):
                speak("I didn't understand that.")
                continue
            if(True in shouldconfirm and (not self.confirm(command, flavor, amount, drink))):
                continue
            print "Command:", command, "Drink:", drink, "Flavor:", flavor, "Amount:", amount
            if(command=='alter'):
                if(not drink):
                    drink = lastdrink
                if(flavor == 'good'):
                    drinks[drink].wasgood()
                elif(flavor == 'bad'):
                    drinks[drink].wasbad()
                    if drinks[drink].hasfailed():
                        drinks.pop(drink)
                else:
                    if(not amount):
                        speak("I didn't understand that.")
                        continue
                    drinks[drink].alter_recipe(flavor, float(amount))
            else:
                if(drink):
                    drinks[drink].make(flavor)
                    lastdrink = drink
                else:
                    if(flavor):
                        #TODO: make drink with that flavor
                        pass
                    else:
##                        newdrink = createnewdrink() #TODO: change this method call
                        drinks[newdrink.name] = newdrink
                        newdrink.make()
                        lastdrink = newdrink.name

    def confirm(self, command, flavor, amount, drink):
        speak = self._speak
        listen = self._listen
        if(command == 'make'):
            if(not drink):
                drink = 'drink'
                if(not flavor):
                    flavor = 'new'
            speak("Do you want me to make you a " + flavor + ' ' + drink + "?")
        else:
            if(drink):
                if(amount > 0):
                    change = 'more'
                else:
                    change = 'less'
                speak("Do you want to make the " + drink + ' ' + change + ' ' + flavor + "?")
        confirmation = ''
        while(confirmation == ''):
            speech = listen()
            while(not speech):
                speak("I didn't hear you.")
                speech = listen()
            confirmation = self._yesnosim.classify(speech)
            if(confirmation == ''):
                speak("I didn't understand that")
        if(confirmation == 'yes'):
            return True
        else:
            return False

    def load_novel_drinks(self):
        pass
        #TODO: open the novel drinks file, read it, return dictionary with
        #keys drink names and values Drink objects

def main():
    cfh = ControlFlowHandler()
    cfh.handle()

if __name__ == '__main__':
    main()