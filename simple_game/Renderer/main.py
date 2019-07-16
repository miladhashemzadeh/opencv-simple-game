import abc
import threading
import time

import cv2
import numpy as np


class Engine:
    def __init__(self, width, height, *, fps=30, game=None):
        self._width = width
        self._fps = fps
        self.game = game
        self._height = height
        self._destroyed = False
        self.frame = self.invalidate()
        self.currentTime = int(time.time())
        self.passedTime = 0
        threading.Thread(target=self._keepWindow).start()

    @abc.abstractmethod
    def draw(self, canvas):
        pass

    def setGame(self, game):
        self.game = game

    def _keepWindow(self):
        while not self._destroyed:
            time.sleep(0.016)
            self.frame = self.draw(self.invalidate())
            key = cv2.waitKey(10)
            cv2.imshow("forrest runner!!!", self.frame)
            if -1 != int(key):
                self._keyboardHited(key)
            if key == 27:
                cv2.destroyAllWindows()
                break

    def setDestroy(self, isDestroy):
        self._destroyed = isDestroy

    def invalidate(self):
        frame = np.zeros((self._height, self._width, 3), np.uint8)
        return frame

    def _keyboardHited(self, key):
        # 32 space
        self.game.onKey(key)
        pass

if __name__ == "__main__":
    #                                                                         ___
    #                                                                       /     \
    # fps is always on 60 and i don't make it right now                   _|_______|_  <-- it's me angry and sad
    # because i'm going to fucking military Service.god damn it             |o | Q|
    Engine(800, 600, fps=30)
