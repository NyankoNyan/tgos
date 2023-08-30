from __future__ import annotations
from .sprite import Sprite
from .common_types import Vector3
import tgos.appcontext


class SceneObject(object):
    __slots = ["sprite", "coord", "context", "parent"]

    def __init__(self,
                 sprite: Sprite = None,
                 coord: Vector3 = Vector3(0, 0, 0),
                 parent: SceneObject = None) -> None:
        self.sprite = sprite
        self.coord = coord
        self.context: tgos.appcontext.AppContext = None
        self.parent = parent

    def draw(self, draw_callback):
        if self.sprite is not None:
            self.sprite.draw(self.glpos.v2, draw_callback)

    @property
    def glpos(self):
        if self.parent is None:
            return self.coord
        else:
            return self.parent.glpos + self.coord
