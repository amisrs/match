import MySQLdb
import numpy as np
from classifier import TfidfEmbeddingVectorizer
import gensim.models as g
from scipy.spatial.distance import cosine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MeanEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        # if a text is empty we should return a vector of zeros
        # with the same dimensionality as all the other vectors
        self.dim = len(word2vec.itervalues().next())

    def fit(self, X, y):
        return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w] for w in words if w in self.word2vec]
                    or [np.zeros(self.dim)], axis=0)
            for words in X
        ])


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
other_query = "SELECT keywords, id FROM course_scrape WHERE university = 'University of Glasgow' and keywords != ''"

other_cursor.execute(other_query)
other_keywords = other_cursor.fetchall()
other_cursor.close()

# print "Loading w2v word embeddings..."
# with open("glove.6B.50d.txt", "rb") as lines:
#     w2v = {line.split()[0]: np.array(map(float, line.split()[1:])) for line in lines}
# print "w2v loaded."

# tfvect = MeanEmbeddingVectorizer(w2v)

unsw_vects = {}
other_vects = {}
print "Loading doc2vec model..."
m = g.Doc2Vec.load("enwiki_dbow/doc2vec.bin")
print "doc2vec model loaded."

print "Vectorizing unsw keywords..."
for unsw_keyword, unsw_id in unsw_keywords:
    unsw_keyword = unsw_keyword.replace("\"", "")
    unsw_keyword = unsw_keyword.split(", ")
    print unsw_keyword
    unsw_vect = m.infer_vector(unsw_keyword, alpha=0.01, steps=1000)
    #unsw_vect = tfvect.transform(unsw_keyword)
    unsw_vects[unsw_id] = unsw_vect

print "Vectorizing other keywords..."
for other_keyword, other_id in other_keywords:
    other_keyword = other_keyword.replace("\"", "")
    other_keyword = other_keyword.split(", ")
    other_vect = m.infer_vector(other_keyword, alpha=0.01, steps=1000)
    #other_vect = tfvect.transform(other_keyword)
    other_vects[other_id] = other_vect

print "Vectorizing complete."

print "Running similarity..."
rows = []
for unsw_vect in unsw_vects:
    print "UNSW Course: " + str(unsw_vect)
    for other_vect in other_vects:
        #sim btwen unsw_vects[unsw_vect] and other_vects[other_vect]

        similarity = cosine(unsw_vects[unsw_vect], other_vects[other_vect])
        rows.append((unsw_vect, other_vect, similarity))
        # insert_query = "INSERT INTO similarity (course1, course2, similarity) VALUES ({0}, {1}, {2}) ON DUPLICATE KEY UPDATE similarity = {2};".format(unsw_vect,other_vect,similarity)
        # insert_cursor = db.cursor()
        # insert_cursor.execute(insert_query);
        # insert_cursor.close()
        # db.commit()

insert_cursor = db.cursor()
noerror = False
while noerror != True:
    try:
        insert_cursor.executemany("INSERT INTO similarity (course1, course2, similarity) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE similarity = VALUES(similarity);", rows)
        noerror = True
    except Exception as e:
        noerror = False

db.commit()

print "Finished execution."
