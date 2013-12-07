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
        penalty -- int, penalty for having the same words in multiple labels (default min(3, number of labels - 1))
        """
        self._instances = {} #dictionary. Key: label, value: Counter of word frequencies
        self._bigram_instances = {} #dictionary. Key: label, value: Counter of bigram frequencies
        self._train(fname, penalty)

    def _train(self, fname, penalty):
        """Reads a file of training data and creates self._instances for future use

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
        instances = self._instances
        bi_inst = self._bigram_instances
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
                bi_freqs = bi_inst[label]
            else:
                word_freqs = Counter()
                bi_freqs = Counter()
            #if google only guessed one thing, copy that thing
            if(not row[1]):
                for i in range(1,5):
                    row[i] = row[0]
            for index, phrase in enumerate(row):
                last_word = ''
                for word in phrase.split():
                    #weight by the order Google guessed it in
                    #i.e. first guesses weighted more
                    word_freqs[word] += 1 / float(index + 1)
                    if(last_word != ''):
                        bi_freqs[last_word + ' ' + word] += 1 / float(index + 1)
                    last_word = word
                instances[label] = word_freqs
                bi_inst[label] = bi_freqs
        csvfile.close
        #reduce weight of words common to many labels
        #find total frequencies of words
        avg_word_freqs = Counter()
        avg_bi_freqs = Counter()
        penalty = min(len(instances) - 1, penalty)
        for label in instances:
            word_freqs = instances[label]
            bi_freqs = bi_inst[label]
            for word in word_freqs:
                #normalize by number of training instances
                word_freqs[word] /= float(num_training_instances[label])
            for bi in bi_freqs:
                bi_freqs[bi] /= float(num_training_instances[label])
            avg_word_freqs += word_freqs
            avg_bi_freqs += bi_freqs
            instances[label] = word_freqs
            bi_inst[label] = bi_freqs
        #convert from total to a multiple of the average
        for word in avg_word_freqs:
            avg_word_freqs[word] *= (penalty / float(len(instances)))
        for bi in avg_bi_freqs:
            avg_bi_freqs[bi] *= (penalty / float(len(bi_inst)))
        #subtract the average frequency of each word
        for label in instances:
            instances[label] -= avg_word_freqs
            bi_inst[label] -= avg_bi_freqs
        self._instances = instances
        self._bigram_instances = bi_inst

    def classify(self, hypotheses, threshold = 0.2, confirm_cushion = 2, bigram_weight = 1):
        """Returns the best label based on word frequencies
        or empty string if confidence doesn't exceed threshhold.
        Second return value is boolean indicating whether the result
        needs to be confirmed or not

        Keyword arguments:
        hypotheses -- result from Google stt to classify
        threshold -- similarity threshold necessary to return a label (default 0.1)
        confirm_cushion -- the multiple of the average that the best similarity
            must be to not have to confirm (default 2)
        bigram_weight -- relative to unigrams, how much bigrams should matter (default 0.5)
        """
        bestsimilarity = 0
        avgsim = 0 #avg similarity
        avgbisim = 0 #avg bigram similarity
        #calculate each label's similarity with the interpeted text
        for label in self._instances:
            word_freqs = self._instances[label]
            bi_freqs = self._bigram_instances[label]
            similarity = 0
            bisimilarity = 0 #similarity based on bigrams
            matched_words = ""
            matched_bigrams = ""
            for index, hypothesis in enumerate(hypotheses):
                phrase = hypothesis['utterance']
                lastword = ''
                for word in phrase.split():
                    #if words match, increase similarity score
                    #weight by the order google guessed them in
                    similarity += word_freqs[word] / float(index + 1)
                    bisimilarity += bi_freqs[lastword + ' ' + word] / float(index + 1)
                    #print matching words
                    if(word_freqs[word] / float(index + 1) > 0):
                        matched_words += "\t" + word + ' %.2f\n' % word_freqs[word]
                    if(bi_freqs[lastword + ' ' + word] / float(index + 1) > 0):
                        matched_bigrams += "\t" + lastword + ' ' + word + ' %.2f\n' % bi_freqs[lastword + ' ' + word]
                    lastword = word
            avgsim += similarity
            avgbisim += bisimilarity
            combinedsim = similarity + bisimilarity * bigram_weight
            if combinedsim >= bestsimilarity:
                bestsimilarity = combinedsim
                bestlabel = label
                print label, 'is the best-----------------------------------'
            print label, '\t%.2f' % similarity
            print label, '\t%.2f' % bisimilarity
            if(matched_words):
                print matched_words
            if(matched_bigrams):
                print matched_bigrams
        avgsim /= len(self._instances)
        avgbisim /= len(self._bigram_instances)
        print ''
        print "Best sim:", bestsimilarity, "Avg sim:", avgsim
        if(bestlabel == 'none'):
            #matched to special 'none' label
            return '', False
        elif(bestsimilarity >= threshold):
            #if bestsim isn't enough higher than the average sim, should confirm
            should_confirm = (bestsimilarity / avgsim < confirm_cushion)
            return bestlabel, should_confirm
        else:
            #nothing matched with sufficient confidence
            return '', False
