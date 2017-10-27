# http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html

from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer

from sklearn.svm import SVC, LinearSVC


from collections import defaultdict

import gensim
import codecs
import numpy as np
import pandas as pd

# Vectorizer from: http://nadbordrozd.github.io/blog/2016/05/20/text-classification-with-word2vec/
class TfidfEmbeddingVectorizer(object):
    def __init__(self, word2vec):
            self.word2vec = word2vec
            self.word2weight = None
            self.dim = len(word2vec.itervalues().next())

    def fit(self, x, y):
        tfidf = TfidfVectorizer(analyzer=lambda x: x)
        tfidf.fit(x)

        max_idf = max(tfidf.idf_)
        self.word2weight = defaultdict(
            lambda: max_idf,
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()]
        )

        return self

    def transform(self, x):
        print x
        return np.array([
            np.mean([self.word2vec[w] * self.word2weight[w]
                for w in words if w in self.word2vec] or
                [np.zeros(self.dim)], axis=0)
            for words in x
        ])

class classifier:
    count_vect = CountVectorizer()
    tfidf_transformer = TfidfTransformer()
    vectorizer = None
    outline_train = load_files('outline_sentences')
    text_clf = None

    def classify_sentence(self, sentence):

        print 'Give me a new sentence:'
        docs_new = ['']
        docs_new[0] = sentence

        # vectorize and balance the new input

        predicted = self.text_clf.predict(docs_new)
        probs = zip(self.outline_train.target_names, self.text_clf.decision_function(docs_new)[0])
        for prob in probs:
            print prob

        classification = ""
        for doc, category in zip(docs_new, predicted):
            classification = self.outline_train.target_names[category]
            print "%r => %s" % (doc, classification)

        return (probs, classification)



    def __init__(self):

        # load w2v word embeddings

        print "Loading w2v word embeddings..."
        with open("glove.6B.50d.txt", "rb") as lines:
            w2v = {line.split()[0]: np.array(map(float, line.split()[1:])) for line in lines}
        print "w2v loaded."
        train_length = 0

        # tfidf = term frequency / inverse document frequency
        # it transforms the counts to be more fair
        # longer documents = less weight
        # very common words across documents = less weight


        # choose a classifier
        # clf = MultinomialNB().fit(outline_train_tfidf, self.outline_train.target)
        self.vectorizer = TfidfEmbeddingVectorizer(w2v)
        self.text_clf = Pipeline([('vect', self.vectorizer),
#                             ('tfidf', TfidfTransformer()),
                            #  ('clf', SGDClassifier(loss='hinge', penalty='l2',
                            #                        alpha=1e-3, random_state=42,
                            #                        max_iter=5, tol=None)),
                            # ('clf', SVC(kernel='linear', probability=True)),
                            ('clf', LinearSVC(tol=0.1)),
                            # ('clf', LogisticRegression(tol=0.1)),

        ])

        print self.text_clf.fit(self.outline_train.data, self.outline_train.target)
        # classify_sentence('hey')
