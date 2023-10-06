from __future__ import annotations
from . import vectors
from copy import copy

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

    @corner.setter
    def corner(self, value: Vector2):
        self.x = value.x
        self.y = value.y

    @property
    def size(self):
        return Vector2(self.width, self.height)

    @size.setter
    def size(self, value: Vector2):
        self.width = value.x
        self.height = value.y

    def __str__(self) -> str:
        return f"{{corner:{self.corner}, size:{self.size}}}"

    def snap_to(self, target: Rect, top: int = None, bottom: int = None, left: int = None, right: int = None) -> Rect:
        result = copy(self)
        if bottom is not None:
            result.y = target.y + bottom
            if top is not None:
                result.height = target.height - top - bottom
        elif top is not None:
            result.y = target.y + target.height - self.height - top

        if left is not None:
            result.x = target.x + left
            if right is not None:
                result.width = target.width - left - right
        elif right is not None:
            result.x = target.x + target.width - self.width - right

        return result


class Borders(object):
    __slots__ = ["l", "r", "t", "b"]

    def __init__(self, l: int = 0, r: int = 0, t: int = 0, b: int = 0) -> None:
        assert l >= 0 and r >= 0 and t >= 0 and b >= 0
        self.l = l
        self.r = r
        self.t = t
        self.b = b
