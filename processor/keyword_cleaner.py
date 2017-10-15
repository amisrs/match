import nltk
import re
import os
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.tag.stanford import StanfordPOSTagger

#https://stackoverflow.com/questions/30821188/python-nltk-pos-tag-not-returning-the-correct-part-of-speech-tag
home = os.getcwd()
_path_to_model = home + '/stanford-postagger/models/english-bidirectional-distsim.tagger'
_path_to_jar = home + '/stanford-postagger/stanford-postagger.jar'



class keyword_cleaner:
    # we don't want to have stupid keywords, like adverbs or adjectives
    # actually we only want nouns?


    good_pos = ['NN', 'NNS', 'NNP', 'NNPS']
    cleaned_list = []
    broken_list = []

    def clean_keywords(self, keywords):
        print 'Cleaning keyword list: '
        blacklist = [
            "student",
            "staff",
            "outcome",
            "course",
            "lecture",
            "class",
            "tutorial",
            "http",
            "teaching",
            "exam",
            "study",
            "email",
            "time",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "feedback",
            "quiz",
            "week",
            "grade",
            "submission",
            "announcement",
            "school",
            "myexperience",
            "learning",
            "understand",
            "assessment",
            "question",
            "bachelor",
            "undergraduate",
            "postgraduate",
            "consultation",
            "please",
            "session",
            "semester",
            "teacher",
            "download",
            "appointment",
            "available",
            "contact",
            "office",
            "phone",
            "may ",
            "website",
            "privacy",
            "library",
            "tutor",
            "access",
            "cohort",
            "portal",
            "enrol",
            "preference",
            "location",
            "login",
            "moodle",
            "consult",
            "enquiries"
            "content",
            "purpose",
            "conclude",
            "marks",
            "university",
            "provide",
            "asterisk",
            "paper"
            "skill",
            "engage",
            "material",
            "instruction",
            "workload",
            "effort",
            "check",
            "satisfy",
            "criteria",
            "conisderation",
            "honest",
            "homework",
            "copies",
            "thought",
            "peers",
            "slides",
            "clear",
            "emphasis",
            "relevant",
            "involve",
            "improve",
            "moderate",
            "result",
            "addition",
            "also",
            "encourage",
            "reading",
            "unsw",
            "attend",
            "must",
            "make",
            "sites",
            "achievement",
            "goals",
            "strongly",
            "choose",
            "calculator",
            "primarily",
            "format",
            "period",
            "maximum",
            "level",
            "participation",
            "details",
            "major",
            "minor",
            "key",
            "plagiarism",
            "conduct",
            "exercises",
            "assignment",
            "interfere",
            "safely",
            "submit",
            "online",
            "absence",
            "resources",
            "personal",
            "seminar",
            "competenc",
            "degree",
            "achieve",
            "safely",
            "misadventure",
            "address",
            "manner",
            "failure",
            "assist",
            "complete",
            "contents",
            "describe",
            "penalt",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            " lic ",
            "supervisor",
            "surprising",
            "scholar",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            "january",
            "february",
            "march",
            "april",
            "june",
            "july",
            "august",
            "september",
            "october",
            "november",
            "december",
            "cannot",
            "kensington",
            "campus",
            "college",
            "university",
            "fortnight",
            "following",
            "help",
            "respon",
            "curriculum",
            "faculty",
            "false",
            "counsel",
            "consider",
            "medical cert",
            "textbook",
            "awarded",
            "incorrect",
            "bookshop",
            "unfair",
            "unsatisfactory",
            "attempt",
            "comprise",
            "see table",
            "see above",
            "see more",
            "see below",
            "receive",
            "propose",
            "prepare",
            "illness",
            "unduly",
            "originals",
            "authenticity",
            "workshop",
            "concession",
            "minimum",
            "require",
            "beyond",
            "highlight",
            "regard",
            "month",
            "work place",
            "workplace",
            "projector",
            "member",
            "cover page",
            "soft copy",
            "transport",
            "printing",
            "footnote",
            "heading",
            "header",
            "grammar",
            "spelling",
            "spacing",
            "page limit",
            "append",
            "points",
            "clarify",
            "confidential",
            "unip",
            "hard copy",
            "medical",
            "academic life",
            "stay safe",
            "blackboard",
            "generally",
            "see part b",
            "discuss",
            "request",
            "permission",
            "taught",
            "learnt",
            "learned",
            "disadvantage",
            "disability",
            "exemption",
            "due date",
            "academic",
            "withdrawal",
            "summary",
            "reflective",
            "reflect",
            "introduction",
            "title page",
            "paragraph",
            "hardcopy",
            "lateness",
            "pastic",
            "envelope",
            "confidential",
            "zero mark",
            "automatically",
            "extension",
            "maths support",
            "ground floor",
            "wide range",
            "including free",
            "supporting documentation",
            "opportunity",
            "echocentre",
            "recordings",
            "elective",
            "meaning",
            "explain",
            "concise",
            "consist",
            "agreed",
            "advise",
            "screen",
            "outline",
            "insist",
            "finish date",
            "start date",
            "indicate",
            "context",
            "actions",
            "limitations",
            "determine",
            "assess",
            "unlikely",
            "count toward",
            "entitle",
            "last minute",
            "cramm",
            "maximise",
            "absent",
            "peer evalu",
            "edition",
            "least nine",
            "activities",
            "mild",
            "unsure",
            "rarely",
            "word doc",
            "turnitin",
            "constitute",
            "duration",
            "select",
            "strengths",
            "weaknesses",
            "mindful",
            "ability",
            "present",
            "commitment",
            "recommend",
            "deadline",
            "finish",
            "practise",
            "skills",
            "made based",
            "one day",
            "paper",
            "topic",
            "module"
        ]
        passed_blacklist = []
        for word in keywords:
            word = word.replace("'", "")
            word = word.replace("\"", "")
            reg = re.compile('\w ')
            if reg.search(word) != None:
                # we don't want to mess with phrases
                if word not in self.cleaned_list:
                    is_black = False
                    for blackword in blacklist:
                        if blackword in word:
                            print blackword + " is in " + word
                            is_black = True
                            break
                    if not is_black and word not in passed_blacklist and len(word) > 5:
                        print word + " passed the blacklist"


                        passed_blacklist.append(word)
                continue

            # now it's only single words
            # st = StanfordPOSTagger(_path_to_model, _path_to_jar)
            # word_pos = st.tag([word])
            if len(word) == 0:
                continue
            word_pos = nltk.pos_tag([word])
            try:
                print word.encode('utf-8', 'ignore') + ' is a ' + word_pos[0][1]
            except UnicodeDecodeError as e:
                continue
            if word_pos[0][1] in self.good_pos:
                if word not in self.cleaned_list:
                    is_black = False
                    for blackword in blacklist:
                        if blackword in word:
                            is_black = True
                            break

                    if not is_black and word not in passed_blacklist and len(word) > 5:
                        passed_blacklist.append(word)

        # st = StanfordPOSTagger(_path_to_model, _path_to_jar)
        # pos_list = st.tag_sents([passed_blacklist])
        #
        # for word, pos in pos_list[0]:
        #     if pos in self.good_pos:
        #         self.cleaned_list.append(word)
        self.cleaned_list = passed_blacklist

        print self.cleaned_list
        return self.cleaned_list

    def break_phrases(self, list_to_break):
        self.broken_list = []

        for word in list_to_break:
            for word_token in word_tokenize(word):
                self.broken_list.append(word_token)
        print self.broken_list
        return self.broken_list

    def compare_keywords(self, list1, list2, sim_type="path"):
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
                        # print "similarity of: " + str(synset1) + " vs " + str(synset2)
                        if sim_type == "path":
                            sim = synset1.path_similarity(synset2)
                        elif sim_type == "lch":
                            sim = synset1.lch_similarity(synset2)
                        elif sim_type == "wup":
                            sim = synset1.wup_similarity(synset2)
                        # elif sim_type == "res":
                        #     sim = synset1.res_similarity(synset2)
                        # elif sim_type == "jcn":
                        #     sim = synset1.jcn_similarity(synset2)
                        # elif sim_type == "lin":
                        #     sim = synset1.lin_similarity(synset2)
                        #
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
