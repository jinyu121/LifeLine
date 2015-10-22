__author__ = 'haoyu'


class Config:
    delayTable = {
        'none': 0,
        'zero': 0,
        'short': 1.5,
        'norm': 2.5,
        'normal': 2.5,
        'long': 3.5,
        'long long': 5
    }
    debug = False
    pause = False
    filename = 'StoryData.txt'

    def debugPrint(message):
        print('debug:=>%s' % message)

    def debugPause():
        input('debug:=>程序暂停，按回车继续')
