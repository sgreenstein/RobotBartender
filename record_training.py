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

def main():
    train_for(['make', 'Rum and Coke'], ['command_training.csv'])
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
