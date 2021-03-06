# Entry point for the classification process.
# This program reads course outlines from the database and breaks them into sentences.
# Then it passes the sentences into the classifier, and writes the result to the database.
# Then it extracts keywords and writes those to the database.

from nltk.tokenize import sent_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

from rake_nltk import Rake

from bs4 import BeautifulSoup
from classifier import classifier
from keyword_cleaner import keyword_cleaner


import re
import MySQLdb

r = Rake()
kc = keyword_cleaner()

with open('mysqlp.txt', 'r') as mysqlp_file:
    mysqlp = mysqlp_file.read().split('\n')[0]

punkt_param = PunktParameters()

# this is so the sentence tokenizer doesn't think that the full stops in abbreviations are end of sentence.
abbreviation = ['Max', 'Min', 'max', 'min', 'e.g', 'i.e', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
punkt_param.abbrev_types = set(abbreviation)

tokenizer = PunktSentenceTokenizer(punkt_param)

classifier = classifier()
db = MySQLdb.connect(host="", user="", passwd=, db="") # don't laugh at me i left credentials in the commit

cursor = db.cursor()

# we skip swansea because it has WAY too many courses and just eats time
cursor.execute("""SELECT * FROM course_scrape WHERE university != "Swansea University" """)
outlines = cursor.fetchall()
# for every course outline
for university, url, text, course_code, course_title, course_id, keywords, emails in outlines:
    # take the 'text' field as input

    outcome_keywords = []

    # I want to destroy non-space whitespace. Otherwise it's hard to determine words.
    text = replace_p = re.sub('<p\s*?>', '', text)
    text = replace_p2 = re.sub('</p>', '. ', text)
    text = replace_div = re.sub('<div\s*?>', '', text)
    text = replace_div2 = re.sub('</div>', '. ', text)
    text = text.replace('\r', '.')
    text = text.replace('\n', ' ')

    cleaned_text = BeautifulSoup(text, "lxml").text
    token_list = tokenizer.tokenize(cleaned_text)

    # Now the course outline is broken into sentences.
    # I want to run in batches so it doesn't restart from the beginning if it crashes
    batch_count = 0
    print "\n========================= Tokens: "+str(len(token_list))+ " ========================="
    for token in token_list:


        token = token.replace("\"", "")

        # Call to classifier.py
        classifier_result = classifier.classify_sentence(token)

        # The probability is not important, doesn't really tell us much
        probs = classifier_result[0]

        # This is the actual result of classification
        classified = classifier_result[1]

        prob_dict = {}
        for cat, prob in probs:
            prob_dict[cat] = prob

        guessed_category = max(prob_dict, key=prob_dict.get)

        # We want keywords only from course outcomes or course content, that were relatively accurately classified.
        if (guessed_category == 'course_outcomes' and abs(prob_dict['course_outcomes']) <= 0.5) or (guessed_category == 'course_content' and abs(prob_dict['course_content']) <= 0.5):
            r.extract_keywords_from_text(token)
            ranked_phrases = r.get_ranked_phrases()
            for phrase in ranked_phrases:
                if len(phrase) < 4:
                    # Don't want short words
                    ranked_phrases.remove(phrase)
            outcome_keywords.extend(list(set(ranked_phrases)))



        insert_cursor = db.cursor()

        # If a sentence has already been classified, just update the values.
        # Otherwise insert new
        get_existing = ("""
            SELECT id FROM sentence WHERE text = \"{0}\" and course = {1}
            """.format(token.replace("\"", "").encode('utf-8', 'ignore'), course_id))
        insert_cursor.execute(get_existing)
        existing_id = insert_cursor.fetchone()
        if existing_id is not None:
            for id_value in existing_id:
                    insert_query = ("""
                        UPDATE sentence SET
                            assessments = {0},
                            contact_hours = {1},
                            course_content = {2},
                            course_outcomes = {3},
                            textbooks = {4},
                            class = \"{5}\"
                        WHERE id = {6}
                        """.format(prob_dict['assessments'],
                                   prob_dict['contact_hours'],
                                   prob_dict['course_content'],
                                   prob_dict['course_outcomes'],
                                   prob_dict['textbooks'],
                                   classified,
                                   id_value)
                    )
        else:
            insert_query = ("""
                INSERT INTO sentence (
                    text,
                    course,
                    assessments,
                    contact_hours,
                    course_content,
                    course_outcomes,
                    textbooks,
                    class
                ) VALUES (\"{0}\", \"{1}\", \"{2}\", \"{3}\", \"{4}\", \"{5}\", \"{6}\", \"{7}\")
                """.format(token.replace("\"", "").encode('utf-8', 'ignore'),
                           course_id,
                           prob_dict['assessments'],
                           prob_dict['contact_hours'],
                           prob_dict['course_content'],
                           prob_dict['course_outcomes'],
                           prob_dict['textbooks'],
                           classified)
            )

        print '\n'
        print insert_query
        insert_cursor.execute(insert_query)
        insert_cursor.close()
        if batch_count >= 50:
            db.commit()
            batch_count = 0

    db.commit()
    keyword_string = ""
    outcome_keywords = kc.clean_keywords(outcome_keywords)
    for keyword in outcome_keywords:
        keyword_string += '"'+keyword.encode("utf-8", "ignore")+'", '

    outline_cursor = db.cursor()
    keyword_query = """UPDATE course_scrape SET keywords = {0} where id = {1}""".format("'"+keyword_string+"'", course_id)

    print keyword_query
    outline_cursor.execute(keyword_query)
    outline_cursor.close()

    db.commit()

cursor.close()
