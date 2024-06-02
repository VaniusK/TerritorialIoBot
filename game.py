
class Game():
    def __init__(self, type, column, row):
        self.stickerSize = 27
        self.startX = 260
        self.startY = 118
        self.xOffset = 132
        self.yOffset = 132
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