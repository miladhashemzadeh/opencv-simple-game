import os
import threading
import time
from random import randint

import cv2

from simple_game.Game.base.Coordinate import Coordinate
from simple_game.Game.base.GameObject import GameObject
from simple_game.Game.base.ObjectGenerator import Player
from simple_game.Renderer.main import Engine

__author__ = "milad"


class Game(Engine):
    def __init__(self, width, height, mode, fps):
        # speed of runner by the mode level and passing the time should change

        face = self.getFace()
        self.player = Player(face, 100, 90)
        self.player.animate()
        self.player.setCoordinate(Coordinate(50, 400))
        global obsSize
        obsSize = 40
        self.currentMode = mode
        self.mode = {"easy": 5, "medium": 4, "hard": 3}
        self.speed = int(12/self.mode.get(self.currentMode))
        self.obstaclesList = []
        self.notEnded = True
        super().__init__(width, height, fps=fps, game=self)
        self.background = self.invalidate()
        threading.Thread(target=self.obstacleGen).start()
        threading.Thread(target=self.obstacleRem).start()
        threading.Thread(target=self.collisionDetection).start()

    def getFace(self):
        cascade = cv2.CascadeClassifier(os.getcwd() + "/simple_game/assets/haarcascade_frontalface_default.xml")
        cap = cv2.VideoCapture(0)
        while True:
            _, frame = cap.read()
            grayimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face = cascade.detectMultiScale(grayimg, 1.3, 5)
            w, y, x, h = (0, 0, 0, 0)
            for (x, y, w, h) in face:
                if w > 0 and h > 0:
                    break
            cap.release()
            break
        return frame[y:y + h, x:x + w]

    def onKey(self, key):
        if key == 32:
            self.player.jump()

    def finishGame(self):
        exit(0)  # this not a good way

    def obstacleGen(self):
        png = os.getcwd() + "/simple_game/assets/character.png"
        img = cv2.imread(png)
        while True:
            time.sleep(int(self.mode.get(self.currentMode)))
            if randint(0, 1) < 1:
                obs = GameObject(img, Coordinate(760, 460), obsSize, obsSize)
                self.obstaclesList.append(obs)

    def obstacleRem(self):
        while True:
            time.sleep(10)
            if len(self.obstaclesList) > 0:
                for obstacle in self.obstaclesList:
                    if obstacle.getCoordinate().x - 1 <= 0:
                        self.obstaclesList.remove(obstacle)

    def moveObjects(self, canvas):
        if len(self.obstaclesList) > 0:
            for obstacle in self.obstaclesList:
                coordinatey = obstacle.getCoordinate().y
                coordinatex = obstacle.getCoordinate().x
                coordinatex -= self.speed
                obstacle.setCoordinate(Coordinate(coordinatex, coordinatey))
                image = obstacle.image
                if coordinatex >= 0:
                    canvas[coordinatey:coordinatey + image.shape[0],
                    coordinatex:coordinatex + image.shape[1]] = image

    def draw(self, canvas):
        # draw player
        self.drawPlayer(canvas)
        # move objects
        self.moveObjects(canvas)

        return canvas

    def drawPlayer(self, canvas):
        coordinate = self.player.getCoordinate()
        image = self.player.getImage()
        canvas[coordinate.y:coordinate.y + image.shape[0],
        coordinate.x:coordinate.x + image.shape[1]] = image

    def collisionDetection(self):
        pass


if __name__ == "__main__":
    # i don't care how many repos is in the github
    # but it feels empty without me X)
    game = Game(800, 600, "hard", fps=30)
