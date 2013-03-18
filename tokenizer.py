#coding=utf-8
import codecs
import os
import mmseg
from weibo import Status

mmseg.Dictionary.dictionaries = (
    ('chars', os.path.join(os.path.dirname(__file__), 'data', 'chars.dic')),
    ('words', os.path.join(os.path.dirname(__file__), 'data', 'words.dic'))
)
mmseg.Dictionary.load_dictionaries()


class Tokenizer(object):
    def __init__(self):
        self.stopwords = set(x.strip() for x in codecs.open(os.path.join('model', 'weibo.stopwords'), 'r', 'utf-8'))

    def __call__(self, str):
        status = Status.wrap(str)
        content = status.get_content()

        algor = mmseg.Algorithm(content)
        tokens = map(lambda x: x.text, algor)

        # append the emo and topic
        for e in status.get_emos():
            algor = mmseg.Algorithm(e)
            tokens.extend(map(lambda x: x.text, algor))

        for t in status.get_topics():
            algor = mmseg.Algorithm(t)
            tokens.extend(map(lambda x: x.text, algor))

        return [x for x in tokens if x not in self.stopwords]


if __name__ == '__main__':
    seg = Tokenizer()
    print " ".join(seg(u'@某某甜品 今天的米没煮 pa ！！好硬~~~[伤心]'))
