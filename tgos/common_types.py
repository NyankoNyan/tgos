from __future__ import annotations
import math
from . import vectors

Vector2 = vectors.V2
Vector3 = vectors.V3

class Rect(object):
    __slots__ = ["x", "y", "width", "height"]

    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def corner(self):
        return Vector2(self.x, self.y)

    @property
    def size(self):
        return Vector2(self.width, self.height)
