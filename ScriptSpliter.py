__author__ = 'haoyu'

from GameBlock import GameBlock


class ScriptSpliter:
    def __init__(self, scriptReader):
        self.reader = scriptReader

    def parse(self):
        blocks = {}
        blockName = 'game null pointer'
        blocks[blockName] = GameBlock(blockName)
        for line in self.reader:
            # 空行，跳过
            if 0 == len(line):
                continue
            # 注释行，跳过
            if line.startswith('//'):
                continue
            # 区块开始
            if line.startswith(':: '):
                blockName = line[3:].strip()
                if blockName not in blocks.keys():
                    blocks[blockName] = GameBlock(blockName)
                continue
            blocks[blockName].scripts.append(line)
        return blocks
