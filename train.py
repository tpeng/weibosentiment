import codecs
from optparse import OptionParser
import re
import itertools
import cPickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from tokenizer import Tokenizer


def chunk(l, n):
    return itertools.izip(*(iter(l),) * n)


class Corpus(object):
    def __init__(self, name, type=0):
        self.name = name
        lines = (x.strip() for x in codecs.open(self.name, 'r', 'utf-8'))
        self.chunks = list(chunk(lines, 3))
        self.type = type

    def __iter__(self):
        for text, categories, _ in self.chunks:
            yield self._trim(text), categories.split(',')[self.type].strip()

    def _trim(self, text):
        return re.sub(r'^[\d|\s]+', '', text)


def train(corpus):
    tokenizer = Tokenizer()
    clf = LinearSVC(verbose=1)
    vectorizer = TfidfVectorizer(tokenizer=tokenizer)
    data = vectorizer.fit_transform(doc[0] for doc in corpus)
    labels = [doc[1] for doc in corpus]
    clf.fit(data, labels)
    return clf, vectorizer

if __name__ == '__main__':
    optparser = OptionParser()
    optparser.add_option("-t", dest="type", default=1, help="train spam or sentiment classifier")

    options, args = optparser.parse_args()
    corpus = Corpus('data/train.txt', int(options.type))
    svc, vectorizer = train(corpus)

    with open('model/model_%s.pkl' %options.type, 'wb') as fid:
        cPickle.dump(svc, fid)
    with open('model/vectorizer_%s.pkl' %options.type, 'wb') as fid:
        cPickle.dump(vectorizer, fid)