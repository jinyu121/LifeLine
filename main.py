__author__ = 'haoyu'

from FileReader import FileReader
from Config import Config
from ScriptSpliter import ScriptSpliter
from GameBlock import GameBlock


class Game:
    def __init__(self, config):
        self.config = config
        fileReader = FileReader(self.config.filename)
        scriptParser = ScriptSpliter(fileReader)
        self.__gameBlocks = scriptParser.parse()
        self.__gameParameter = {}

    def run(self):
        blockName = 'Start'
        while blockName != 'game null pointer':
            blockName, self.__gameParameter = self.__gameBlocks[blockName].execute(self.__gameParameter)


if __name__ == '__main__':
    config = Config()
    game = Game(config)
    game.run()
