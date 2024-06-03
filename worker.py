from selenium import webdriver
from PIL import Image
from io import BytesIO
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import pytesseract
import math
import base64
import collections
import time
import cv2
from game import Game


class Worker:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.url = "https://territorial.io"
        self.driver.get(self.url)
        self.actions = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 10)  # Wait until page is loaded
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self.pointerX = 0
        self.pointerY = 0
        self.interval = 0.0001

    def makeScreenshot(self):
        canvas_data_url = self.driver.execute_script("return document.getElementById('canvasA').toDataURL();")
        base64_data = canvas_data_url.split(",")[1]
        decoded_data = base64.decodebytes(base64_data.encode("utf-8"))
        img = Image.open(BytesIO(decoded_data))
        return img
    def getColorOfPixel(self, cords):
        x, y = cords

        javascript_function = """
        function getPixelColor(canvas, x, y) {
            var ctx = canvas.getContext('2d');
            var imageData = ctx.getImageData(x, y, 1, 1);
            var data = imageData.data;
            return [data[0], data[1], data[2]];
        }
        """
        javascript_code = f"{javascript_function} return getPixelColor(document.getElementById('canvasA'), {x}, {y});"
        color = self.driver.execute_script(javascript_code)
        return color

    def moveCursor(self, cords):
        width = self.driver.execute_script('return document.documentElement.scrollWidth')
        height = self.driver.execute_script('return document.documentElement.scrollHeight')
        x, y = cords
        x = x * width / 1920
        y = y * height / 812
        self.actions.move_by_offset(x - self.pointerX, y - self.pointerY)
        self.pointerX = x
        self.pointerY = y

    def clickOnPosition(self, cords):
        self.moveCursor(cords)
        self.actions.click()
        self.actions.perform()

    def ifLoading(self):

        for x in range(939, 944):
            for y in range(432, 437):
                color = self.getColorOfPixel((x, y))
                if color == [255, 255, 255]:
                    return True
        return False

    def setName(self, name):
        self.clickOnPosition((950, 400))
        self.actions.key_down(Keys.CONTROL).key_down("A").key_up("A").key_up(Keys.CONTROL).perform()
        self.actions.send_keys(name).perform()
        element = self.wait.until(EC.presence_of_element_located((By.ID, "usernameField")))

        self.wait.until(lambda driver: "Player" not in element.get_attribute('value'))

    def adjustSettings(self):
        self.clickOnPosition((1832, 40))
        time.sleep(self.interval)
        self.clickOnPosition((380, 245))
        time.sleep(self.interval)
        self.clickOnPosition((1175, 350))
        time.sleep(self.interval)
        self.clickOnPosition((50, 750))
        time.sleep(self.interval)
        self.clickOnPosition((50, 750))

    def enterMultiplayer(self):

        field = self.driver.find_element(By.ID, "usernameField")
        self.clickOnPosition((800, 500))
        self.wait.until(EC.staleness_of(field))
        while self.ifLoading():
            time.sleep(self.interval)
        print("Entered Multiplayer")
    def getColorDifference(self, color1, color2):
        return abs(color1[0] - color2[0]) + abs(color1[1] - color2[1]) + abs(color1[2] - color2[2])

    def recognizeGame(self, screenshot, cords):
        interestingColors = {
            "crownColor": [246, 229, 117],
            "blackTeamColor": [0, 1, 2],
            "redTeamColor": [114, 14, 15],
            "greenTeamColor": [9, 116, 13],
            "blueTeamColor": [13, 17, 121],
            "yellowTeamColor": [116, 118, 15],
            "pinkTeamColor": [113, 12, 117],
            "cyanTeamColor": [9, 116, 117],
            "grayTeamColor": [113, 116, 117],
            "white": [255, 255, 255],
            "skullColor": [242, 242, 242],
            "medalColor": [211, 139, 0]
        }
        colors = collections.Counter()
        width, height = 49, 49
        for x in range(0, width):
            for y in range(0, height):
                color = screenshot.getpixel((cords[0] + x, cords[1] + y))
                for key in interestingColors.keys():
                    if "Team" in key:
                        dist = math.sqrt(abs(x - 23) ** 2 + abs(y - 23) ** 2)
                        if dist > 14:
                            continue
                    a = list(interestingColors[key])
                    b = list(color)
                    diff = self.getColorDifference(a, b)
                    if diff < 30:
                        colors[key] += 1


        if colors["skullColor"] >= 270:
            return "PVE"
        if colors["white"] >= 96:
            return "FFA_capped"
        if colors["crownColor"] >= 127:
            return "FFA"
        if colors["medalColor"] >= 65:
            return "Ranked"
        teams = 0
        for key in interestingColors:
            if "Team" in key:
                if colors[key] >= 10:
                    teams += 1
        return str(teams) + " Teams"

    def getCurrentGames(self):
        screenshot = self.makeScreenshot()
        amountOfGames = 6
        games = []
        for i in range(amountOfGames):
            game = Game("", i % 4, i // 4)
            game.type = self.recognizeGame(screenshot, game.getJoinPosition())
            games.append(game)
        return games

    def ifInGame(self):
        color = self.getColorOfPixel((1853, 122))
        return color == [255, 120, 100]

    def joinGame(self, game: Game):
        joinPosition = game.getJoinPosition()
        self.clickOnPosition((joinPosition[0] + 3, joinPosition[1] + 3))
        print("Joining", game)
        while not self.ifInGame():
            time.sleep(self.interval)
        print("Joined")

    def waitForGame(self, allowedTypes):
        while True:
            games = self.getCurrentGames()
            foundGame = False
            for game in games:
                if game.type in allowedTypes:
                    self.joinGame(game)
                    foundGame = True
                    break
            if foundGame:
                break
            time.sleep(1)
