from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from itertools import product
import numpy as np

def break_phrases(list_to_break):
    broken_list = []

    for word in list_to_break:
        for word_token in word_tokenize(word):
            broken_list.append(word_token)
    # print broken_list
    return broken_list

# usage: keyword_similarities = compare_keywords(uni1_keywords, uni2_keywords)
# That returns a list of values for similarity for each element in uni1_keywords.
# You can do an avg or whatever to get a aggregate value

def compare_keywords(list1, list2, sim_type="path"):

    if type(list1) == type("str"):
        list1 = list1.replace("\"", "")
        list1 = list1.split(", ")

    if type(list2) == type("str"):
        list2 = list2.replace("\"", "")
        list2 = list2.split(", ")


    # maximum similarity for each word in list1 with words in list2
    similarity_dict = {}
    similarity_list = []

    # broken_list1 = break_phrases(list1)
    # broken_list2 = break_phrases(list2)
    #https://stackoverflow.com/questions/30829382/check-the-similarity-between-two-words-with-nltk-with-python
    # allsyns1 = set(ss for word in list1 for ss in wordnet.synsets(word))
    # allsyns2 = set(ss for word in list2 for ss in wordnet.synsets(word))
    #
    # for syn1 in allsyns1:
    #     max_syn1 = 0
    #     for syn2 in allsyns2:
    #
    #         sim = wordnet.path_similarity(syn1, syn2)
    #         # print str(syn1) + " vs " + str(syn2) + " = " + str(sim)
    #         if sim > max_syn1:
    #             max_syn1 = sim
    #     similarity_list.append(max_syn1)
    # return similarity_list
    #
    #


    for list1_word in break_phrases(list1):
        try:
            max_similarity = 0
            synsetlist1 = wordnet.synsets(list1_word.encode('utf-8', 'ignore'))
            if len(synsetlist1) == 0:
                continue

            for list2_word in break_phrases(list2):
                # print list2_word.encode('utf-8', 'ignore')
                try:
                    synsetlist2 = wordnet.synsets(list2_word.encode('utf-8', 'ignore'))
                    #calc similarity
                    if len(synsetlist2) == 0:
                        continue

                    syn_sum = 0
                    avg_similarity = 0

                    print "For " + list1_word + " vs " + list2_word
                    # print "Comparing synset1: " + str(synsetlist1)
                    # print "to synset2: " + str(synsetlist2)
                    best = max((wordnet.wup_similarity(s1, s2) or 0, s1, s2) for s1, s2 in
                            product(synsetlist1, synsetlist2))
                    print best
                    print "\n"

                    if best[0] > max_similarity:
                        max_similarity = best[0]
                except Exception as e:
                    print "Exception: " + str(e)
                    continue
                # for synset1 in synsetlist1:
                #     synset1sum = 0
                #     for synset2 in synsetlist2:
                #         # print "similarity of: " + str(synset1) + " vs " + str(synset2)
                #         if sim_type == "path":
                #             sim = synset1.path_similarity(synset2)
                #         elif sim_type == "lch":
                #             sim = synset1.lch_similarity(synset2)
                #         elif sim_type == "wup":
                #             sim = synset1.wup_similarity(synset2)
                #         # elif sim_type == "res":
                #         #     sim = synset1.res_similarity(synset2)
                #         # elif sim_type == "jcn":
                #         #     sim = synset1.jcn_similarity(synset2)
                #         # elif sim_type == "lin":
                #         #     sim = synset1.lin_similarity(synset2)
                #         #
                #         if sim != None:
                #             if sim > max_syn:
                #                 max_syn = sim
                #
                #             synset1sum += sim
                #     synset1avg = synset1sum / len(synsetlist2)
                #     syn_sum += synset1avg
                # avg_similarity = syn_sum / len(synsetlist1)
                #
                #
                # # print list1_word.encode('utf-8', 'ignore') + " similarity to " + list2_word.encode('utf-8', 'ignore') + ": " + str(avg_similarity)
                # if avg_similarity > max_similarity:
                #     max_similarity = avg_similarity

            max_sim_obj = {}
            similarity_dict[list1_word] = max_similarity
            # similarity_list.append(max_sim_obj)
        except Exception as e:
            print "Exception: " + str(e)
            continue
    return similarity_dict

def simdict_avg(simdict):
    vals = []
    for sim in simdict:
        vals.append(simdict[sim])

    return np.mean(vals)
