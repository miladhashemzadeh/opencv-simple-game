import abc

import cv2


class GameObject(abc.ABC):

    def __init__(self, image, coordinate, width, height):
        self.width = width
        self.height = height
        self.image = cv2.resize(image, (width, height))
        self.coordinate = coordinate

    def crashed(self):
        pass

    def getCoordinate(self):
        return self.coordinate

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def setHeight(self, height):
        self.height = height

    def setWidth(self, width):
        self.width = width

    def setCoordinate(self, coordinate):
        self.coordinate = coordinate
