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
def train_for(labels, filenames):
##def train_for(label):
    """Records training data and saves it in a csv file

    Keyword arguments:
    labels -- list of the python labels to associate with the words spoken
    filenames -- list of the filenames in which to save training instances
    """
    stt = stt_google
    csvfiles = []
    writers = []
    for index, filename in enumerate(filenames):
        csvfiles.append(open(filename, 'ab'))
        writers.append(csv.writer(csvfile))
    # record instances until it doesn't interpret any text
    speech = stt.listen_for_speech()
    while(speech):
        for label in labels:
            hypotheses = [label]
            for hypothesis in speech:
                hypotheses.append(hypothesis['utterance'])
            #write hypotheses
            writer.writerow(hypotheses.insert(0, label))
            speech = stt.listen_for_speech()
    csvfile.write('\n')
    csvfile.close
    csvfile2.close

if __name__ == '__main__':
    main()
