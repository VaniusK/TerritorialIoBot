from worker import Worker
import pytesseract
import cv2
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL import Image
import numpy as np
import time
class Player(Worker):
    def __init__(self):
        super().__init__()
        self.myBorderColor = None
        self.myColor = None
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def getInterest(self, screenshot):
        try:
            screenshot = screenshot.crop((1812, 114, 1901, 140))
            interest = float(pytesseract.image_to_string(screenshot, lang="eng", config="outputbase nobatch digits --psm 6"))
            interest *= 0.01
            return interest
        except ValueError:
            return 0.0

    def getIncome(self, screenshot):
        try:
            screenshot = screenshot.crop((1812, 140, 1901, 165))
            income = int("0" + pytesseract.image_to_string(screenshot, lang="eng", config="outputbase nobatch digits --psm 6"))
            return income
        except ValueError:
            return 0

    def getMoney(self, screenshot):
        try:
            screenshot = screenshot.crop((920, 18, 1165, 59))
            money = int("0" + pytesseract.image_to_string(screenshot, lang="eng", config="outputbase nobatch digits --psm 6"))
            return money
        except ValueError:
            return 0

    def ZoomIn(self):
        self.clickOnPosition((1870, 356))

    def ZoomOut(self):
        self.clickOnPosition((1870, 456))

    def chooseStartLocation(self):
        # Random location
        while self.ifInGame():
            time.sleep(self.interval)
        self.startGame()

    def startGame(self):
        x = 30
        y = 93
        for i in range(11):
            if self.getColorDifference(self.getColorOfPixel((x, y)), (21, 98, 20)) <= 50:
                self.clickOnPosition((x, y))
                print(i)
                break
            y += 32
        for _ in range(10):
            self.ZoomOut()
        self.myColor = self.getColorOfPixel((960, 406))
        self.myBorderColor = self.getColorOfPixel((960, 401))
        print(self.myColor, self.myBorderColor)
        self.gameCycle()

    def gameCycle(self):
        while True:
            screenshot = self.makeScreenshot()
            money = self.getMoney(screenshot)
            interest = self.getInterest(screenshot)
            income = self.getIncome(screenshot)
            land = income
            effectiveLimit = land * 100
            limit = land * 150
            print(money, interest, income)
            edgesMap = self.generateEdgesMap(screenshot)
            edgesMap.show()
            screenshot.show()
            time.sleep(5)

    def generateEdgesMap(self, screenshot):
        img_array = np.array(screenshot)

        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        edges = cv2.Canny(gray, 50, 150)

        edgesMap = Image.fromarray(edges)

        return edgesMap




