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

    def setGame(self, game):
        self.game = game

    def _keepWindow(self):
        while not self._destroyed:
            time.sleep(0.016)
            key = cv2.waitKey(10)
            cv2.imshow("forrest runner!!!", self.frame)
            if -1 != int(key):
                self._keyboardHited(key)
            if key == 27:
                break
        cv2.destroyAllWindows()

    def setDestroy(self, isDestroy):
        self._destroyed = isDestroy

    def setFrame(self, frame):
        self.frame = frame

    def getFrame(self):
        return self.frame

    def invalidate(self):
        frame = np.zeros((self._height, self._width, 3), np.uint8)
        return frame

    def _keyboardHited(self, key):
        # 32 space
        self.game.onKey(key)
        pass


if __name__ == "__main__":
    #                                                                          _
    #                                                                        /   \
    # fps is always on 60 and i don't make it right now                    _|_____|_  <-- it's me wondering and angry
    # because i'm going to fucking military Service.god damn it             |o | Q|
    Engine(800, 600, fps=30)
