# Working similarity calculator
# This program calculates the similarity between the keywords of EVERY unsw course
# and EVERY other course.
#
# After many attempts, I finally thought of this solution that doesn't take thousands
# of hours to run.
#
# It takes 1-2 hours to run with 4000 courses and 234 unsw courses, ending up with
# over a million rows in the similarity table.
# That's pretty fast!
# https://stackoverflow.com/questions/8897593/similarity-between-two-text-documents

import MySQLdb
import numpy as np
from classifier import TfidfEmbeddingVectorizer
import gensim.models as g
from scipy.spatial.distance import cosine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open('mysqlp.txt', 'r') as mysqlp_file:
    mysqlp = mysqlp_file.read().split('\n')[0]

db = MySQLdb.connect(host="104.236.9.215", user="scraper", passwd=mysqlp, db="scrape")

unsw_cursor = db.cursor()
unsw_query = "SELECT keywords, id FROM course_scrape WHERE university = 'University of New South Wales'"
unsw_cursor.execute(unsw_query)
unsw_keywords = unsw_cursor.fetchall()
unsw_cursor.close()

other_cursor = db.cursor()
# other_query = "SELECT keywords, id FROM course_scrape WHERE university != 'University of New South Wales' and university != 'Swansea University' and keywords != ''"
other_query = "SELECT keywords, id FROM course_scrape WHERE university NOT IN ('University of New South Wales', 'Swansea University', 'University of Glasgow', 'University of Auckland') and keywords != ''"

other_cursor.execute(other_query)
other_keywords = other_cursor.fetchall()
other_cursor.close()


unsw_vects = {}
other_vects = {}
print "Loading doc2vec model..."
m = g.Doc2Vec.load("enwiki_dbow/doc2vec.bin")
print "doc2vec model loaded."

vectorizer = TfidfVectorizer()
for unsw_keyword, unsw_id in unsw_keywords:
    rows = []

    print "Processing UNSW Course: " + str(unsw_id)
    for other_keyword, other_id in other_keywords:

        tfidf = vectorizer.fit_transform([unsw_keyword, other_keyword])

	# cosine distance
        similarity = ((tfidf * tfidf.T).A)[0,1]

        rows.append((unsw_id, other_id, similarity))

    noerror = False

    while noerror != True:
        try:
            insert_cursor = db.cursor()
            insert_cursor.executemany("INSERT INTO similarity (course1, course2, similarity) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE similarity = VALUES(similarity);", rows)
            noerror = True
        except Exception as e:
            print str(e)
            db = MySQLdb.connect(host="104.236.9.215", user="scraper", passwd=mysqlp, db="scrape")
            noerror = False

    db.commit()

print "Finished execution."
