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
    train_for('alcohol', '0.1')
##    train_for('Gin Buck')
def train_for(label, label2):
##def train_for(label):
    """Records training data and saves it in a csv file

    Keyword arguments:
    label -- the python label to associate with the words spoken
    """
    stt = stt_google
    speech = stt.listen_for_speech()
    csvfile = open('flavor_training.csv', 'ab')
    csvfile2 = open('amount_training.csv', 'ab')
    writer = csv.writer(csvfile)
    writer2 = csv.writer(csvfile2)
    # record instances until it doesn't interpret any text
    while(speech):
        hypotheses = [label]
        hypotheses2 = [label2]
        for hypothesis in speech:
            hypotheses.append(hypothesis['utterance'])
            hypotheses2.append(hypothesis['utterance'])
        #print hypotheses
        writer.writerow(hypotheses)
        writer2.writerow(hypotheses2)
        speech = stt.listen_for_speech()
    csvfile.write('\n')
    csvfile.close
    csvfile2.close

if __name__ == '__main__':
    main()
