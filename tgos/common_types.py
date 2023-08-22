from __future__ import annotations
import math


class Vector2(object):
    __slots__ = ["x", "y"]

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    @property
    def sqrmag(self) -> float:
        return self.x**2 + self.y**2

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.sqrmag)

    @property
    def normalized(self) -> Vector2:
        return self / self.magnitude

    def __add__(self, v):
        if isinstance(v, int) or isinstance(v, float):
            return Vector2(self.x + v, self.y + v)
        elif isinstance(v, tuple):
            return Vector2(self.x + v[0], self.y + v[1])
        else:
            return Vector2(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return self + v * -1

    def __mul__(self, v):
        return Vector2(self.x * v, self.y * v)
    
    def __truediv__(self, v):
        return self * (1/v)

    def __eq__(self, v):
        return self.x == v.x and self.y == v.y


class Vector3(object):
    __slots__ = ["x", "y", "z"]

    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    @property
    def sqrmag(self) -> float:
        return self.x**2 + self.y**2 + self.y**2

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.sqrmag)

    @property
    def normalized(self) -> Vector3:
        return self / self.magnitude

    def __eq__(self, __value: object) -> bool:
        return (self.x == __value.x
                and self.y == __value.y
                and self.z == __value.z)

    def __add__(self, v):
        if isinstance(v, int):
            return Vector3(self.x + v, self.y + v, self.z + v)
        elif isinstance(v, tuple):
            return Vector3(self.x + v[0], self.y + v[1], self.z + v[2])
        else:
            return Vector3(self.x + v.x, self.y + v.y, self.z + v.z)

    def __mul__(self, v):
        return Vector3(self.x*v, self.y*v, self.z*v)

    def __sub__(self, v):
        return self + v * -1

    @property
    def v2(self) -> Vector2:
        return Vector2(self.x, self.y)


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
