__author__ = 'haoyu'

import time
import re
from Config import Config


class GameBlock:
    def __init__(self, name):
        self.name = name
        self.scripts = []
        self.nextName = 'game null pointer'
        self.__jumpNow = False
        self.__if = [True]
        self.__silently = False
        self.__choicesJump = []
        self.__choicesShow = []
        self.__choices = 0

    def __doChoice(self, script):
        tagStart = script.find('[[')
        tagPipe = script.find('|')
        tagEnd = script.find(']]')
        key = script[tagPipe + 1:tagEnd].strip()
        value = script[tagStart + 2:tagPipe].strip()
        self.__choicesJump.append(key)
        self.__choicesShow.append(value)
        self.__choices += 1

    def __doIf(self, script):
        parameter = self.__parameter
        script = script.replace('<<if', '')
        script = script.replace('<<elseif', '')
        script = script.replace('>>', '')
        script = script.replace(' is ', ' == ')
        script = script.replace(' eq ', ' == ')
        script = script.replace(' gte ', ' >= ')
        script = re.sub(r'\$(\S+)', r'parameter["\1"]', script)
        script = script.strip()
        judgeResult = eval(script)
        if Config.debug:
            Config.debugPrint(script)
            Config.debugPrint(judgeResult)

        self.__if[-1] = judgeResult

    def __doElse(self, script):
        self.__if[-1] = not self.__if[-1]

    def __doEndIf(self, script):
        self.__if.pop()

    def __doJudge(self, script):
        if script.startswith('<<if'):
            self.__if.append(True)
            self.__doIf(script)
            return
        if script.startswith('<<elseif'):
            self.__doIf(script)
            return
        if script.startswith('<<endif'):
            self.__doEndIf(script)
            return
        if script.startswith('<<else'):
            self.__doElse(script)
            return

    def __doJump(self, script):
        if script.startswith('[[delay'):
            pipPosition = script.find('|')
            self.nextName = script[pipPosition + 1:-2]
            self.__delay(timeDelay='long', busy=True)
        else:
            self.nextName = script[2:-2]
        if Config.debug:
            Config.debugPrint(self.nextName)
        self.__jumpNow = True

    def __doSet(self, script):
        parameter = self.__parameter
        script = script.replace('<<set ', '')
        script = script.replace('>>', '')
        script = re.sub(r'\$(\S+)', r'parameter["\1"]', script)
        script = script.strip()
        exec(script)
        if Config.debug:
            Config.debugPrint(script)
        self.__parameter = parameter

    def __doSilently(self, script):
        self.__silently = script.startswith('<<silently')

    def __doPrintParameter(self, script):
        tagStart = script.find('$')
        tagEnd = script.find('>>')
        parameter = script[tagStart + 1:tagEnd]
        try:
            parameter = self.__parameter[parameter]
        except:
            parameter = ''
        print('\b%s' % parameter, end='')

    def __doScript(self, script):
        if script.startswith('<<if') or script.startswith('<<elseif') or \
                script.startswith('<<endif') or script.startswith('<<else'):
            self.__doJudge(script)
            return
        if self.__if[-1]:
            if script.startswith('[['):
                self.__doJump(script)
                return
            if script.startswith('<<silently') or script.startswith('<<silently'):
                self.__doSilently(script)
                return
            if script.startswith('<<choice'):
                self.__doChoice(script)
                return
            if script.startswith('<<set'):
                self.__doSet(script)
                return
            if script.startswith('<<$'):
                self.__doPrintParameter(script)
                return

    def __makeChoice(self):
        self.__delay()
        print()
        for i in range(0, self.__choices):
            print('%d => %s' % (i + 1, self.__choicesShow[i]))
        choice = 0
        while True:
            try:
                choice = int(input('做出选择：')) - 1
                if choice < 0 or choice > 1:
                    raise
                print()
                break
            except:
                continue
        self.nextName = self.__choicesJump[choice]

    def __delay(self, timeDelay='norm', busy=False):
        delay = 1.5
        if isinstance(timeDelay, int):
            delay = timeDelay
        elif isinstance(timeDelay, str):
            if timeDelay not in Config.delayTable.keys():
                timeDelay = 'norm'
            delay = Config.delayTable[timeDelay]
        if Config.debug:
            delay = 0
        if busy:
            print()
            print('[泰勒忙碌]')
            print()
        time.sleep(delay)

    def execute(self, parameter):
        if Config.debug:
            Config.debugPrint(self.name)
        self.__parameter = parameter
        for script in self.scripts:
            if Config.pause:
                Config.debugPause()
            if script.startswith('<<') or script.startswith('[['):
                self.__doScript(script)
                if self.__choices == 2:
                    self.__makeChoice()
                    break
                continue
            if self.__if[-1]:
                self.__delay()
                print(script)
            if self.__jumpNow:
                break
        return self.nextName, self.__parameter
