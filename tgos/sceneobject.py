from __future__ import annotations
from .sprite import Sprite
from .common_types import Vector3
import tgos.appcontext

class SceneObject(object):
    __slots = ["sprite", "coord", "context"]

    def __init__(self, sprite: Sprite = None, coord: Vector3 = Vector3(0, 0, 0)) -> None:
        self.sprite = sprite
        self.coord = coord
        self.context: tgos.appcontext.AppContext = None

    def draw(self, draw_callback):
        self.sprite.draw(self.coord.v2, draw_callback)
