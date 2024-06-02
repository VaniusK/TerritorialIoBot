from selenium import webdriver
from PIL import Image
from io import BytesIO
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import collections
import time
from game import Game
class Worker():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = "https://territorial.io"
        self.driver.get(self.url)
        self.actions = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 10)  # Wait until page is loaded
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self.pointerX = 0
        self.pointerY = 0

    def makeScreenshot(self):
        screenshot = self.driver.get_screenshot_as_png()
        img = Image.open(BytesIO(screenshot))  # Convert the screenshot into an image object
        img = img.resize((self.driver.execute_script("return document.body.clientWidth"),
              self.driver.execute_script("return window.innerHeight")))
        return img

    def clickOnPosition(self, cords):
        x, y = cords
        self.actions.move_by_offset(x - self.pointerX, y - self.pointerY)
        self.pointerX = x
        self.pointerY = y
        self.actions.click()
        self.actions.perform()

    def ifLoading(self):
        screenshot = self.makeScreenshot()
        whites = 0
        for x in range(500, 551):
            for y in range(250, 301):
                color = screenshot.getpixel((x, y))
                if color == (255, 255, 255):
                    whites += 1
        return whites >= 50
    def setName(self, name):
        self.clickOnPosition((500, 260))
        self.actions.key_down(Keys.CONTROL).key_down("A").key_up("A").key_up(Keys.CONTROL).perform()
        self.actions.send_keys(name).perform()

    def enterMultiplayer(self):
        screenshot = self.makeScreenshot()
        img = screenshot.crop((0, 0, 400, 320))
        #img.show()
        self.clickOnPosition((400, 320))
        while self.ifLoading():
            time.sleep(1)
        print("Entered Multiplayer")

    def recognizeGame(self, screenshot):
        interestingColors = {
            "crownColor": (246, 229, 117),
            "blackTeamColor": (0, 1, 2),
            "redTeamColor": (114, 14, 15),
            "greenTeamColor": (9, 116, 13),
            "blueTeamColor": (13, 17, 121),
            "yellowTeamColor": (116, 118, 15),
            "pinkTeamColor": (113, 12, 117),
            "cyanTeamColor": (9, 116, 117),
            "grayTeamColor": (113, 116, 117),
            "white": (255, 255, 255),
            "skullColor": (242, 242, 242),
            "medalColor": (211, 139, 0)
        }
        colors = collections.Counter()
        width, height = screenshot.size
        for x in range(0, width):
            for y in range(0, height):
                color = screenshot.getpixel((x, y))
                for key in interestingColors.keys():
                    a = list(interestingColors[key])
                    b = list(color)
                    diff = abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
                    if diff < 20:
                        colors[key] += 1

        if colors["crownColor"] == 32:
            return "FFA"
        if colors["white"] == 20:
            return "FFA_capped"
        if colors["skullColor"] == 70:
            return "PVE"
        if colors["medalColor"] == 24:
            return "Ranked"
        if colors["grayTeamColor"] >= 10 and colors["blackTeamColor"] >= 10:
            return "8 Teams"  # maybe 7. Who knows
        if colors["cyanTeamColor"] >= 10:
            return "6 Teams"
        if colors["pinkTeamColor"] >= 10:
            return "5 Teams"
        if colors["yellowTeamColor"] >= 10:
            return "4 Teams"
        if colors["blueTeamColor"] >= 10:
            return "3 Teams"
        if colors["greenTeamColor"] >= 10:
            return "2 Teams"



    def getCurrentGames(self):
        windowSize = self.driver.get_window_size()
        screenshot = self.makeScreenshot()
        amountOfGames = 6
        games = []
        for i in range(amountOfGames):
            game = Game("", i % 4, i // 4)
            game.type = self.recognizeGame(screenshot.crop(game.getStickerBox()))
            games.append(game)
        return games

    def joinGame(self, game: Game):
        self.clickOnPosition(game.getJoinPosition())
        print("Joined", game)
        time.sleep(5)
        img = self.makeScreenshot()
        img.show()

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

