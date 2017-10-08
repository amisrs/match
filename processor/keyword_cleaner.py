import nltk
import re

from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize

class keyword_cleaner:
    # we don't want to have stupid keywords, like adverbs or adjectives
    # actually we only want nouns?
    good_pos = ['NN', 'NNS', 'NNP', 'NNPS']
    cleaned_list = []
    broken_list = []

    def clean_keywords(self, keywords):
        print 'Cleaning keyword list: '
        print keywords
        for word in keywords:
            reg = re.compile('\w ')
            if reg.search(word) != None:
                # we don't want to mess with phrases

                self.cleaned_list.append(word)
                continue

            # now it's only single words
            word_pos = nltk.pos_tag([word])
            print word + ' is a ' + word_pos[0][1]
            if word_pos[0][1] in self.good_pos:
                self.cleaned_list.append(word)
        return self.cleaned_list

    def break_phrases(self, list_to_break):
        self.broken_list = []

        for word in list_to_break:
            for word_token in word_tokenize(word):
                self.broken_list.append(word_token)
        print self.broken_list
        return self.broken_list

    def compare_keywords(self, list1, list2):
        similarity_list = []

        for list1_word in list1:
            max_similarity = 0
            synsetlist1 = wordnet.synsets(list1_word)
            if len(synsetlist1) == 0:
                continue

            for list2_word in list2:
                synsetlist2 = wordnet.synsets(list2_word)
                #calc similarity
                if len(synsetlist2) == 0:
                    continue

                syn_sum = 0
                avg_similarity = 0

                for synset1 in synsetlist1:
                    synset1sum = 0
                    for synset2 in synsetlist2:
                        print "similarity of: " + str(synset1) + " vs " + str(synset2)
                        sim = synset1.path_similarity(synset2)
                        if sim != None:
                            synset1sum += sim
                    synset1avg = synset1sum / len(synsetlist2)
                    syn_sum += synset1avg
                avg_similarity = syn_sum / len(synsetlist1)


                print list1_word + " similarity to " + list2_word + ": " + str(avg_similarity)
                if avg_similarity > max_similarity:
                    max_similarity = avg_similarity

            max_sim_obj = {list1_word: max_similarity}
            similarity_list.append(max_sim_obj)
        return similarity_list
