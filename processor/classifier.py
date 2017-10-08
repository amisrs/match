from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC, LinearSVC

from mlxtend.plotting import plot_decision_regions

from collections import defaultdict

import gensim
import codecs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
        # outline_new_counts = self.count_vect.transform(docs_new)
        # outline_new_tfidf = self.tfidf_transformer.transform(outline_new_counts)

        predicted = self.text_clf.predict(docs_new)
        # print self.outline_train.target_names
        # print self.text_clf.predict_proba(docs_new)
        probs = zip(self.outline_train.target_names, self.text_clf.predict_proba(docs_new)[0])
        for prob in probs:
            print prob

        for doc, category in zip(docs_new, predicted):
            print "%r => %s" % (doc, self.outline_train.target_names[category])

        return probs



    def __init__(self):

        # load w2v word embeddings

        print "Loading w2v word embeddings..."
        with open("/media/sf_share/glove.6B/glove.6B.50d.txt", "rb") as lines:
            w2v = {line.split()[0]: np.array(map(float, line.split()[1:])) for line in lines}
        print "w2v loaded."
        train_length = 0
        #
        # print 'Loading doc2vec wiki model...'
        # model = '/media/sf_share/enwiki_dbow/doc2vec.bin'
        # doc2vec_model = gensim.models.Doc2Vec.load(model)
        # print 'doc2vec loaded.'

        # print 'Vectorizing test files...'
        # categories = ['contact_hours', 'textbooks']
        #
        # for category in categories
        # print '-> Splitting sentences into words...'
        # vector_docs = [ x.strip().split() for x in codecs.open(test_files, 'r', 'utf-8').readlines() ]
        #
        # print '-> Writing vectors to output...'
        # output = open('doc_vectors.txt', 'w+')
        # outline_train_counts = numpy.zeros(len(vector_docs))
        # for d in vector_docs:
        #     outline_train_counts.append(' '.join([str(x) for x in doc2vec_model.infer_vector(d, alpha=0.01, steps=1000)]))
        #
        # output.flush()
        # output.close()
        #
        # print 'Vectorizing complete.'

        # CountVectorizer is a bag of words vectorizer
        # The vector is based on the count of occurrences
        # count_vect = CountVectorizer()
        # tfidf_transformer = TfidfTransformer()


        # outline_train = load_files('outline_sentences')
        # outline_train_counts = self.count_vect.fit_transform(outline_train.data)

        # tfidf = term frequency / inverse document frequency
        # it transforms the counts to be more fair
        # longer documents = less weight
        # very common words across documents = less weight
        # outline_train_tfidf = self.tfidf_transformer.fit_transform(outline_train_counts)


        # choose a classifier
        # clf = MultinomialNB().fit(outline_train_tfidf, self.outline_train.target)
        self.vectorizer = TfidfEmbeddingVectorizer(w2v)
        self.text_clf = Pipeline([('vect', self.vectorizer),
#                             ('tfidf', TfidfTransformer()),
                            #  ('clf', SGDClassifier(loss='hinge', penalty='l2',
                            #                        alpha=1e-3, random_state=42,
                            #                        max_iter=5, tol=None)),
                            ('clf', SVC(kernel='linear', probability=True)),
                            # ('clf', LinearSVC()),

        ])

        print self.text_clf.fit(self.outline_train.data, self.outline_train.target)
        # classify_sentence('hey')
