from sprite import Sprite
from common_types import Vector3


class SceneObject(object):
    __slots = ["sprite", "coord"]

    def __init__(self, sprite: Sprite = None, coord: Vector3 = Vector3(0, 0, 0)) -> None:
        self.sprite = sprite
        self.coord = coord

    def draw(self, draw_callback):
        self.sprite.draw(self.coord.v2, draw_callback)
