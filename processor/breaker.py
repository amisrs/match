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
abbreviation = ['Max', 'Min', 'max', 'min', 'e.g', 'i.e', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
punkt_param.abbrev_types = set(abbreviation)

tokenizer = PunktSentenceTokenizer(punkt_param)

classifier = classifier()
db = MySQLdb.connect(host="104.236.9.215", user="scraper", passwd=mysqlp, db="scrape")
cursor = db.cursor()

# cursor.execute("""SELECT * FROM course_scrape WHERE university != 'cityofhongkong' and university != 'mcgill' and university != 'newcastle' and university != 'sheffield' and university != 'ubc' and university != 'swansea' and university != 'University of Sussex' and university != 'Lancaster University' and university != 'University of Leeds' LIMIT 2""")
cursor.execute("""SELECT * FROM course_scrape WHERE keywords = "" """)

outlines = cursor.fetchall()
# for every course outline
for university, url, text, course_code, course_title, course_id, keywords, emails in outlines:
    # take the 'text' field as input

    outcome_keywords = []

    print university
    text = replace_p = re.sub('<p\s*?>', '', text)
    text = replace_p2 = re.sub('</p>', '. ', text)
    text = replace_div = re.sub('<div\s*?>', '', text)
    text = replace_div2 = re.sub('</div>', '. ', text)
    text = text.replace('\r', '.')
    text = text.replace('\n', ' ')

    cleaned_text = BeautifulSoup(text, "lxml").text
    token_list = tokenizer.tokenize(cleaned_text)

    batch_count = 0
    print "\n========================= Tokens: "+str(len(token_list))+ " ========================="
    for token in token_list:
        # print token
        token = token.replace("\"", "")
        classifier_result = classifier.classify_sentence(token)
        probs = classifier_result[0]
        classified = classifier_result[1]

        prob_dict = {}
        for cat, prob in probs:
            prob_dict[cat] = prob

        guessed_category = max(prob_dict, key=prob_dict.get)

        if (guessed_category == 'course_outcomes' and abs(prob_dict['course_outcomes']) <= 0.5) or (guessed_category == 'course_content' and abs(prob_dict['course_content']) <= 0.5):
            r.extract_keywords_from_text(token)
            ranked_phrases = r.get_ranked_phrases()
            for phrase in ranked_phrases:
                if len(phrase) < 4:
                    ranked_phrases.remove(phrase)
            outcome_keywords.extend(list(set(ranked_phrases)))



        insert_cursor = db.cursor()

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

    # break
        # pass to classifier
