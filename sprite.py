from image import Image


class Sprite(object):
    __slots__ = ["image", "anchor"]

    def __init__(self, image: Image, anchor: list = (.5, .5)) -> None:
        assert (image != None)
        self.image = image
        self.anchor = anchor


class GameObject(object):
    __slots = ["sprite", "coord"]

    def __init__(self, sprite: Sprite = None, coord: list = (0, 0)) -> None:
        self.sprite = sprite
        self.coord = coord
