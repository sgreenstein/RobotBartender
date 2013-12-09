#-------------------------------------------------------------------------------
# Name:        record_training
# Purpose:     records speech and saves to file for training later
#
# Author:      SGreenstein
#
# Created:     30/11/2013
# Copyright:   (c) SGreenstein 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import stt_google
import csv
import create_presets
from ingredient import Ingredient
import time

def main():
##    train_for(['alter', 'Rum and Coke', 'alcoholic'], ['command_training.csv', 'drink_training.csv', 'flavor_training.csv'])
    #make me a <drink>
 ##   train_many('make', drinks = create_presets.getdrinks())
    #make me a <flavor> drink
  ##  train_many('make', flavors = Ingredient.flavorlist())
    #make me a <flavor> <drink>
    train_many('make', drinks = create_presets.getdrinks(), flavors = Ingredient.flavorlist())
 ##   train_many('make', drinks = ['Cuba Libre'], flavors = ['sour'])
    #that drink was too <flavor>
##    train_many('alter', flavors = Ingredient.flavorlist())
##    train_many('alter', flavors = ['sour'])
    #that <drink> was too <flavor>
##    train_many('alter', drinks = create_presets.getdrinks(), flavors = Ingredient.flavorlist())
    #that drink was <bad/good>
##    train_many('alter', flavors = ['bad', 'good'])
    #that <drink> was <bad/good>
##    train_many('alter', drinks = create_presets.getdrinks(), flavors = ['bad', 'good'])

def train_many(command, drinks = {'none':'none'}, flavors = ['none']):
    """Records training data for many drinks and flavors and saves it in a csv file

    Keyword arguments:
    command -- command label to train for
    drinks -- list of drinks to train for (default all presets)
    flavors -- list of flavor labels to train for (default all)
    """
    try:
        flavors.remove('flavor_strength') #don't need to train for flavor_strength
    except:
        pass
    stt = stt_google
    amounts = ['0.1', '-0.1']
    filenames = ['command_training.csv', 'drink_training.csv', 'flavor_training.csv']
    csvfiles = []
    writers = []
    for index, filename in enumerate(filenames):
        currfile = open(filename, 'ab')
        csvfiles.append(currfile)
        writers.append(csv.writer(currfile))
    if(command == 'alter' and not ('bad' in flavors) and not ('good' in flavors)):
        currfile = open('amount_training.csv', 'ab')
        csvfiles.append(currfile)
        writers.append(csv.writer(currfile))
    # record instances until it doesn't interpret any text
    has_speech = True
    while(has_speech):
        for drink in drinks:
            if(not has_speech):
                break
            for flavor in flavors:
                if(not has_speech):
                    break
                try:
                    if(drinks[drink].level_of(flavor) == 0):
                        #don't train if it doesn't have the flavor
                        continue
                except:
                    pass
                for amount in amounts:
                    labels = [command, drink, flavor]
                    if(command == 'alter' and not ('bad' in flavors) and not ('good' in flavors)):
                        labels.append(amount)
                    _print_instructions(command, drink, flavor, amount)
                    speech = stt.listen_for_speech()
                    if(not speech):
                        has_speech = False
                        break
                    hypotheses = []
                    for hypothesis in speech:
                        hypotheses.append(hypothesis['utterance'])
                    #write hypotheses
                    for index, label in enumerate(labels):
                        writers[index].writerow([label] + hypotheses)
    for csvfile in csvfiles:
        csvfile.close

def _print_instructions(command, drink, flavor, amount):
    """Prints a message telling the user what to say for training
    """
    if(command == 'alter'):
        if(drink == 'none'):
            drink = 'that'
        if(flavor == 'bad' or flavor == 'good'):
            print drink, "was", flavor
        else:
            if(float(amount) > 0):
                print drink, "wasn't", flavor, 'enough'
            else:
                print drink, "was too", flavor
    else:
        if(drink == 'none'):
            drink = 'something'
        if(flavor == 'none'):
            flavor = ''
        print "Make", flavor, drink
    time.sleep(0.5)

def train_for(labels, filenames):
    """Records training data and saves it in a csv file

    Keyword arguments:
    labels -- list of the python labels to associate with the words spoken
    filenames -- list of the filenames in which to save training instances
    """
    stt = stt_google
    csvfiles = []
    writers = []
    for index, filename in enumerate(filenames):
        currfile = open(filename, 'ab')
        csvfiles.append(currfile)
        writers.append(csv.writer(currfile))
    # record instances until it doesn't interpret any text
    speech = stt.listen_for_speech()
    while(speech):
        hypotheses = []
        for hypothesis in speech:
            hypotheses.append(hypothesis['utterance'])
        #write hypotheses
        for index, label in enumerate(labels):
            writers[index].writerow([label] + hypotheses)
        speech = stt.listen_for_speech()
    for csvfile in csvfiles:
        csvfile.close

if __name__ == '__main__':
    main()
