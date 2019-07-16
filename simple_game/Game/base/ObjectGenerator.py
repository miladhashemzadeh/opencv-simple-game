import threading
import time

import cv2
import numpy as np

from fun_game.simple_game.Game.base.Coordinate import Coordinate
from fun_game.simple_game.Game.base.GameObject import GameObject


class Player(GameObject):

    def __init__(self, face, width, height):
        self.isJumping = True
        self.legs = None
        self.isCrashed = False
        self.face = face
        self.body = np.zeros((int(height / 3), width, 3), np.uint8)
        self.standLegs = np.zeros((int(height / 2), width, 3), np.uint8)
        self.openedLegs = np.zeros((int(height / 2), width, 3), np.uint8)
        self.width = width
        self.height = height
        self.legsIsOpen = True
        self.remainingHeight = 0
        self.remainingWidth = 0
        self.makeBody(face, width, height)
        self.playerBody = np.zeros((self.height + self.remainingHeight, self.width + self.remainingWidth, 3), np.uint8)
        self.legs = self.openedLegs
        self.game = None
        image = self.getImage()
        self.setWidth(image.shape[1])
        self.setHeight(image.shape[0])
        self.animate()
        self.legAnimator = threading.Thread(target=self.startAnimating).start()
        self.jumpThread = jumpThread(self)
        self.jumpThread.start()

    def crashed(self):
        self.isCrashed = True

    def setGame(self, game):
        self.game = game

    def setFace(self, face):
        self.face = face

    def jump(self):
        self.jumpThread.jump()

    def getFace(self):
        return self.face

    def animate(self):
        if self.isCrashed:
            self.boomEndGame()
        time.sleep(.2)
        self.animateLeg()

    def getImage(self):
        self.playerBody[:self.face.shape[0], 37:self.face.shape[1] + 37] = self.face
        self.playerBody[self.face.shape[0]:self.face.shape[0] + self.body.shape[0], :self.body.shape[1]] = self.body
        self.playerBody[self.body.shape[0] + self.face.shape[0]:self.face.shape[0] + self.body.shape[0] + self.legs.shape[0],
        :self.legs.shape[1]] = self.legs
        return self.playerBody

    def makeBody(self, face1, width, height):
        legHeight = int(height / 2)
        faceHeight = int(face1.shape[1] / 5)
        whiteColor = (255, 255, 255)
        stroke = 2
        # scale face
        try:
            self.face = cv2.resize(face1, (int(width / 3), faceHeight))
            self.remainingWidth += int(width / 4)
            self.remainingHeight += int(face1.shape[1] / 7)
        except cv2.error:
            self.face = np.zeros((30, 30, 3), np.uint8)
            cv2.circle(self.face, (15, 15), 15, (255, 255, 255), 1)
            cv2.circle(self.face, (7, 10), 2, (255, 255, 255), 1)
            cv2.circle(self.face, (20, 10), 2, (255, 255, 255), 1)
            cv2.line(self.face, (5, 25), (25, 20), (255, 255, 255), 1)
            self.remainingHeight += 31
            self.remainingWidth += width
        # body
        cv2.line(self.body, (int(width / 2), 0), (width - int(width * 0.3), int(legHeight / 2)), whiteColor, stroke)
        cv2.line(self.body, (int(width * 0.3), int(legHeight / 2)), (int(width / 2), 0), whiteColor, stroke)
        cv2.line(self.body, (int(width / 2), 0), (int(width / 2), height), whiteColor, stroke)
        # one leg
        cv2.line(self.standLegs, (int(width / 2), 0), (int(width / 2), height), whiteColor, stroke)
        # two leg
        cv2.line(self.openedLegs, (0, height), (int(width / 2), 0), whiteColor, stroke)
        cv2.line(self.openedLegs, (int(width / 2), 0), (width, height), whiteColor, stroke)

    def animateLeg(self):
        if self.legsIsOpen:
            self.legs = self.standLegs
            self.legsIsOpen = False
        else:
            self.legs = self.openedLegs
            self.legsIsOpen = True

    def startAnimating(self):
        while 1:
            self.animate()

    def boomEndGame(self):
        self.game.finishGame()


class jumpThread(threading.Thread):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.isJumping = True
        self.lock = threading.Lock()

    def jump(self):
        if self.lock.locked():
            self.isJumping = False
            self.lock.release()

    def run(self) -> None:
        super().run()
        while True:
            self.lock.acquire()
            if not self.isJumping:
                self.isJumping = True
                for i in range(25, 1, -3):
                    time.sleep(.2)
                    coordinate = self.player.getCoordinate()
                    coordinate.y -= i
                    self.player.setCoordinate(coordinate)
                for i in range(1, 25, 3):
                    time.sleep(.2)
                    coordinate = self.player.getCoordinate()
                    coordinate.y += i
                    self.player.setCoordinate(coordinate)
                self.isJumping = False
                self.player.setCoordinate(Coordinate(50, 400))


if __name__ == "__main__":
    pass
