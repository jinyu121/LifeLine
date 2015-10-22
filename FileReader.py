__author__ = 'haoyu'


class FileReader:
    def __init__(self, filename):
        self.filename = filename
        self.__script = []
        self.__readScripts()

    def __recordScript2(self, script):
        script = script.replace(chr(65279), '').strip()
        if len(script) > 0:
            if script != '|':
                self.__script.append(script)

    def __recordScript(self, script):
        script = script.replace(chr(65279), '').strip()
        if len(script) > 0:
            if script != '|':
                if script.find(']]>>') >= 0:
                    self.__recordScript2(script)
                else:
                    while script.find('[[') >= 0:
                        positinStart = script.find('[[')
                        positionEnd = script.find(']]')
                        self.__recordScript2(script[0:positinStart])
                        self.__recordScript2(script[positinStart:positionEnd + 3])
                        script = script[positionEnd + 3:]
                    self.__recordScript2(script)

    def __readScripts(self):
        try:
            __FILE = open(self.filename)
            for script in __FILE:
                while script.find('<<') >= 0:
                    labelStart = script.find('<<')
                    labelEnd = script.find('>>')
                    self.__recordScript(script[0:labelStart])
                    self.__recordScript(script[labelStart: labelEnd + 2])
                    script = script[labelEnd + 2:]
                self.__recordScript(script)
            __FILE.close()
        except:
            print('加载游戏脚本出错')
            raise

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.__script.pop(0).strip().strip(chr(65279))
        except:
            raise StopIteration


if __name__ == '__main__':
    FILENAME = 'StoryDataSmall.txt'
    scriptReader = FileReader(FILENAME)
    for x in scriptReader:
        print(x)
