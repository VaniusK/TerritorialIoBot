
class Game():
    def __init__(self, type, column, row):
        self.stickerSize = 45
        self.startX = 547
        self.startY = 184
        self.xOffset = 211
        self.yOffset = 211
        self.gamesPerRow = 4

        self.type = type
        self.column = column
        self.row = row

    def __str__(self):
        return f"{self.type}, {self.column} column, {self.row} row"

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.type)}, {self.column}, {self.row})"

    def getJoinPosition(self):
        x = self.startX + self.column * self.xOffset
        y = self.startY + self.row * self.yOffset
        return (x, y)
    def getStickerBox(self):
        joinPosition = self.getJoinPosition()
        return joinPosition + (joinPosition[0] + self.stickerSize, joinPosition[1] + self.stickerSize)