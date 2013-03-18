#coding=utf-8
import cPickle


class Classifier(object):
    def __init__(self, type):
        with open('model/model_%s.pkl' % type, 'rb') as fid:
            self.model = cPickle.load(fid)
        with open('model/vectorizer_%s.pkl' % type, 'rb') as fid:
            self.vectorizer = cPickle.load(fid)

    def classify(self, str):
        data = self.vectorizer.transform([str])
        return self.model.predict(data)[0]

if __name__ == '__main__':
    classifier = Classifier(1)
    print classifier.classify(u'纪梵希的绅士香水 还蛮好闻的')
    print classifier.classify(u'The Body Shop 美体小铺保湿芳香露莓沐浴胶 http://t.cn/zOA2ujT')
    print classifier.classify(
        u'【闺蜜今日推荐】：仅售65元抢购！雅诗兰黛多层次瞬透保湿霜15ml(中-混)，蕴含雅诗兰黛独有的全新Bio-Mimetic Water多元矿物精华水，激发肌肤的天然保湿屏障，轻松深入肌肤补水，瞬间肌肤重获活力，宛如新生！您能即刻感受到补水锁水的神奇功效！任意两单全国包邮！ http://t.cn/heRbfq')
    print classifier.classify(u'@某某甜品 今天的米没煮 pa ！！好硬~~~[伤心]')
    print classifier.classify(u'谢谢推荐，这个系列的作者是 @rickjin ， 可以在这个链接下看目前为止的5个章节，还有两个章节待续： http://t.cn/zlH3Ygc')
    print classifier.classify(
        u'欧莱雅 青春密码精华肌底液30ml[嘻嘻]款欧莱雅雪颜淡斑祛斑霜精华30ml[嘻嘻]欧莱雅~完美净白日夜淡斑精华30ml[嘻嘻] 欧莱雅清润全日保湿眼部凝露 15ml[汗]你呀现在还剩多少钱撒？有钱就全买，没钱2，3里面挑一样吧，实在没钱那我也没办法。[抓狂] @Jinn在IELTS苦海中奮鬥')

    classifier = Classifier(0)
    print classifier.classify(u'纪梵希的绅士香水 还蛮好闻的')
    print classifier.classify(u'The Body Shop 美体小铺保湿芳香露莓沐浴胶 http://t.cn/zOA2ujT')
    print classifier.classify(
        u'【闺蜜今日推荐】：仅售65元抢购！雅诗兰黛多层次瞬透保湿霜15ml(中-混)，蕴含雅诗兰黛独有的全新Bio-Mimetic Water多元矿物精华水，激发肌肤的天然保湿屏障，轻松深入肌肤补水，瞬间肌肤重获活力，宛如新生！您能即刻感受到补水锁水的神奇功效！任意两单全国包邮！ http://t.cn/heRbfq')
    print classifier.classify(u'谢谢推荐，这个系列的作者是 @rickjin ， 可以在这个链接下看目前为止的5个章节，还有两个章节待续： http://t.cn/zlH3Ygc')
    print classifier.classify(
        u'欧莱雅 青春密码精华肌底液30ml[嘻嘻]款欧莱雅雪颜淡斑祛斑霜精华30ml[嘻嘻]欧莱雅~完美净白日夜淡斑精华30ml[嘻嘻] 欧莱雅清润全日保湿眼部凝露 15ml[汗]你呀现在还剩多少钱撒？有钱就全买，没钱2，3里面挑一样吧，实在没钱那我也没办法。[抓狂] @Jinn在IELTS苦海中奮鬥')
