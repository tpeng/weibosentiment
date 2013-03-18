#coding=utf-8
from copy import copy
import unittest
import re


class Status(object):
    def __init__(self):
        self.replies = []
        self.urls = []
        self.topics = []
        self.emos = []
        self.content = ''

    def get_replies(self):
        return self.replies

    def get_urls(self):
        return self.urls

    def get_topics(self):
        return self.topics

    def get_emos(self):
        return self.emos

    def get_content(self):
        return self.content

    @staticmethod
    def wrap(str):
        status = Status()
        content = copy(str)
        for to_m in re.finditer(r'@([\w|-]+)', str, re.U):
            status.replies.append(to_m.group(1))
            content = content.replace(str[to_m.start(1) - 1:to_m.end(1)], '')

        for url_m in re.finditer(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str,
                                 re.I):
            status.urls.append(url_m.group())
            content = content.replace(url_m.group(), '')

        for topic_m in re.finditer(r'#(.*?)#', str, re.U):
            status.topics.append(topic_m.group(1))
            content = content.replace(str[topic_m.start(1) - 1:topic_m.end(1) + 1], '')

        for emo_m in re.finditer(r'\[(.*?)\]', str, re.U):
            status.emos.append(emo_m.group(1))
            content = content.replace(str[emo_m.start(1) - 1:emo_m.end(1) + 1], '')

        status.content = content
        return status


class StatusTest(unittest.TestCase):
    def test_wrap_at(self):
        origin = u'#尚品网-----爱TA就将 @进行到底 #我的爱情宣言“将爱情进行到底”，喜欢“迪奥水之欢淡香水”，浓浓玫瑰的味道，香味持久' \
                 u' @尚品网官方微博 @神仙何处 @顺其自然之 @嘘--小欠 @苗雪珊 @悠然黄昏 @-Peter-Pan @蓉儿妹子 ' \
                 u'@淘气的小花猫 @Carrie_Lee @风雨蔚蓝 @refcbjh @雨林景洪 @mint126 @曹宝莹 @小优521 @美茜cookie'
        status = Status.wrap(origin)
        self.assertEqual(18, len(status.get_replies()))
        self.assertEqual(u'进行到底', status.get_replies()[0])
        self.assertEqual(u'美茜cookie', status.get_replies()[-1])

    def test_wrap_url(self):
        origin = u'最新美国直邮回契尔氏不含碱性泡沫洁面乳500ml, http://t.cn/h5nVvY'
        status = Status.wrap(origin)
        self.assertEqual(0, len(status.get_replies()))
        self.assertEqual('http://t.cn/h5nVvY', status.get_urls()[0])

    def test_wrap_topic(self):
        origin = u'#淘宝网购# 雅芳走珠【香水9ML】融合多种花果香 ￥18元 地址： http://t.cn/hdmfzW 推荐理由：携带方便 推荐指数[太阳][太阳][太阳]'
        status = Status.wrap(origin)
        self.assertEqual(1, len(status.get_topics()))
        self.assertEqual(u'淘宝网购', status.get_topics()[0])

    def test_wrap_emo(self):
        origin = u'#淘宝网购# 雅芳走珠【香水9ML】融合多种花果香 ￥18元 地址： http://t.cn/hdmfzW 推荐理由：携带方便 推荐指数[太阳][太阳][太阳]'
        status = Status.wrap(origin)
        self.assertEqual(3, len(status.get_emos()))
        self.assertEqual(u'太阳', status.get_emos()[0])
        self.assertEqual(u'太阳', status.get_emos()[-1])
        self.assertEqual(u' 雅芳走珠【香水9ML】融合多种花果香 ￥18元 地址：  推荐理由：携带方便 推荐指数', status.get_content())

    def test_wrap_em2(self):
        origin = u'小爱妈力推给产后的妈妈咪们！[威武]生完宝宝皮肤都很干，特别是在母乳的妈妈咪，希思黎真的很强大，从左往右，明星产品全能乳液，' \
                 u'明星产品花香化妆水，百合洁面乳！[爱你]小样是瞬间保湿面膜，超好用，准备来支大滴，[哈哈]还有修护面霜。' \
                 u'[威武]小爱妈皮肤是超级过敏型，所以大家可以放心使用！[爱你]'
        status = Status.wrap(origin)
        self.assertEqual(5, len(status.get_emos()))
        self.assertEqual(u'威武', status.get_emos()[0])
        self.assertEqual(u'爱你', status.get_emos()[1])
        self.assertEqual(u'哈哈', status.get_emos()[2])
        self.assertEqual(u'威武', status.get_emos()[3])
        self.assertEqual(u'爱你', status.get_emos()[4])

    def test_wrap(self):
        origin = u'#DHC#紧致焕肤美容霜 [花]原价320，现价224[原价]Q10也是DHC家的明星产品。有亲前两天跟我要面霜哈，这个是可以紧致焕肤滴。' \
                 u'看看喜欢不。推荐指数[太阳][太阳] http://t.cn/hFZ9G 要是有乐啊优惠券，还能免运费哦。详情请见 http://t.cn/hFZ9q'
        status = Status.wrap(origin)
        self.assertEqual(1, len(status.get_topics()))
        self.assertEqual(u'DHC', status.get_topics()[0])

        self.assertEqual(4, len(status.get_emos()))
        self.assertEqual(u'花', status.get_emos()[0])
        self.assertEqual(u'原价', status.get_emos()[1])
        self.assertEqual(u'太阳', status.get_emos()[2])
        self.assertEqual(u'太阳', status.get_emos()[3])

        self.assertEqual(2, len(status.get_urls()))
        self.assertEqual(u'http://t.cn/hFZ9G', status.get_urls()[0])
        self.assertEqual(u'http://t.cn/hFZ9q', status.get_urls()[1])


if __name__ == '__main__':
    unittest.main()