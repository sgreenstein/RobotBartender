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
    train_for('MindEraser.make()')

def train_for(command):
    """Records training data and saves it in a csv file

    Keyword arguments:
    command -- the python command to execute after hearing similar words spoken
    """
    stt = stt_google
    speech = stt.listen_for_speech()
    csvfile = open('drink_training.csv', 'ab')
    writer = csv.writer(csvfile)
    # record instances until it doesn't interpret any text
    while(speech):
        hypotheses = [command]
        for hypothesis in speech:
            hypotheses.append(hypothesis['utterance'])
        #print hypotheses
        writer.writerow(hypotheses)
        speech = stt.listen_for_speech()
##    csvfile.write('\n')
    csvfile.close

if __name__ == '__main__':
    main()
