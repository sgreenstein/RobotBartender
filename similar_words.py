#-------------------------------------------------------------------------------
# Name:        SimilarWords
# Purpose:      checks finds the label with phrases most similar to a
#               phrase interpreted by sst
#
# Author:      SGreenstein
#
# Created:     30/11/2013
# Copyright:   (c) SGreenstein 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import csv
import stt_google
from collections import Counter

class SimilarWords:

    def __init__(self, fname, penalty = 3):
        """Returns an instance of SimilarWords for finding the best label for a phrase

        Keyword arguments:
        fname -- string, specifies csv file of training data
        penalty -- int, penalty for having the same words in multiple labels (default 3)
        """
        self.instances = {} #dictionary. Key: label, value: Counter of word frequencies
        self._train(fname, penalty)

    def _train(self, fname, penalty):
        """Reads a file of training data and creates self.instances for future use

        Keyword arguments:
        fname -- string, filename of csv file with training data
        training data is of the following format:
            label1, hypothesis number one, hypothesis number two,
            label1, hypothesis one,
            label2, hypothesis one, et cetera
        penalty -- int, penalty for having the same words in multiple labels
        """
        #open file
        csvfile = open(fname, 'rb')
        reader = csv.reader(csvfile)
        instances = self.instances
        num_training_instances = Counter()
        #read file into correct format, counting weighted word frequencies
        for row in reader:
            label = row.pop(0)
            #keep up with how many examples of this label there are.
            #Used later for normalization so that labels with more
            #training examples aren't selected more often
            num_training_instances[label] += 1
            if(label in instances):
                word_freqs = instances[label]
            else:
                word_freqs = Counter()
            #if google only guessed one thing, copy that thing
            if(not row[1]):
                for i in range(1,5):
                    row[i] = row[0]
            for index, phrase in enumerate(row):
                for word in phrase.split():
                    #weight by the order Google guessed it in
                    #i.e. first guesses weighted more
                    word_freqs[word] += 1 / float(index + 1)
                instances[label] = word_freqs
        csvfile.close
        #reduce weight of words common to many labels
        #find total frequencies of words
        avg_word_freqs = Counter()
        for label, word_freqs in instances.iteritems():
            for word in word_freqs:
                #normalize by number of training instances
                word_freqs[word] /= float(num_training_instances[label])
            avg_word_freqs += word_freqs
            instances[label] = word_freqs
        #convert from total to a multiple of the average
        for word in avg_word_freqs:
            avg_word_freqs[word] *= (penalty / float(len(instances)))
        #subtract the average frequency of each word
        for label in instances:
            instances[label] -= avg_word_freqs
        self.instances = instances


    def classify(self, hypotheses, threshold = 0.5):
        """Returns the best label based on word frequencies
        or empty string if confidence doesn't exceed threshhold

        Keyword arguments:
        hypotheses -- result from Google stt to classify
        threshold -- similarity threshold necessary to return a label (default 0.5)
        """
        bestsimilarity = 0
        for label, word_freqs in self.instances.iteritems():
            similarity = 0
            matched_words = ""
            for index, hypothesis in enumerate(hypotheses):
                phrase = hypothesis['utterance']
                for word in phrase.split():
                    similarity += word_freqs[word] / float(index + 1)
                    if(word_freqs[word] / float(index + 1) > 0):
                        matched_words += "\t" + word + ' %.2f\n' % word_freqs[word]
            if similarity >= bestsimilarity:
                bestsimilarity = similarity
                bestlabel = label
            print label, '\t%.2f' % similarity
            if(matched_words):
                print matched_words
        print ''
        if(bestsimilarity >= threshold):
            return bestlabel
        else:
            return ''

##    def regress(self, hypotheses):
##        """Finds the best label based on word frequencies.
##        Label is a numeric, continuous data type, not discrete
##
##        Keyword arguments:
##        hypotheses -- result from Google stt to classify
##        """
##        bestlabel = 0
##        for label, word_freqs in self.instances.iteritems():
##            print label
##            similarity = 0
##            for index, hypothesis in enumerate(hypotheses):
##                phrase = hypothesis['utterance']
##                for word in phrase.split():
##                    similarity += word_freqs[word] / float(index + 1)
##                    if(word_freqs[word] / float(index + 1) > 0):
##                        print word, word_freqs[word]
##            bestlabel += float(label) * similarity
##        print similarity
##        return bestlabel
##def main():
##    stt = stt_google
##    sim = SimilarWords('drink_training.csv')
##    print sim.classify(stt.listen_for_speech())
##
##if __name__ == "__main__":
##    main()