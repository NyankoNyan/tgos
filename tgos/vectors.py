from __future__ import annotations
from functools import reduce
from itertools import zip_longest
import math


def vadd(v1: list, v2: list) -> list:
    return [e1+e2 for e1, e2 in zip_longest(v1, v2, fillvalue=0)]


def vsub(v1: list, v2: list) -> list:
    return [e1-e2 for e1, e2 in zip_longest(v1, v2, fillvalue=0)]


def vmul(v1: list, v2: list) -> list:
    return [e1*e2 for e1, e2 in zip_longest(v1, v2, fillvalue=0)]


def vdiv(v1: list, v2: list) -> list:
    return [e1/e2 for e1, e2 in zip_longest(v1, v2, fillvalue=0)]


def vdot(v1: list, v2: list):
    return reduce(lambda a, b: a+b, vmul(v1, v2))


class V(object):
    __slots__ = ["m"]

    def __init__(self, m: list) -> None:
        self.m = m

    @staticmethod
    def c(m):
        return V(m)

    def __eq__(self, v: object) -> bool:
        if isinstance(v, (list, tuple)):
            m = v
        else:
            m = v.m
        return all(map(lambda p: p[0] == p[1], zip_longest(self.m, m, fillvalue=0)))

    def __add__(self, v) -> V:
        if isinstance(v, (list, tuple)):
            return self.c(vadd(self.m, v))
        elif hasattr(v, "m"):
            return self.c(vadd(self.m, v.m))
        else:
            return self.c([e+v for e in self.m])

    def __sub__(self, v) -> V:
        if isinstance(v, (list, tuple)):
            return self.c(vsub(self.m, v))
        elif hasattr(v, "m"):
            return self.c(vsub(self.m, v.m))
        else:
            return self.c([e-v for e in self.m])

    def __mul__(self, v) -> V:
        if isinstance(v, (list, tuple)):
            return self.c(vmul(self.m, v))
        elif hasattr(v, "m"):
            return self.c(vmul(self.m, v.m))
        else:
            return self.c([e*v for e in self.m])

    def __truediv__(self, v) -> V:
        if isinstance(v, (list, tuple)):
            return self.c(vdiv(self.m, v))
        elif hasattr(v, "m"):
            return self.c(vdiv(self.m, v.m))
        else:
            return self.c([e/v for e in self.m])

    def __str__(self) -> str:
        return str(self.m)

    def __repr__(self) -> str:
        return repr(self.m)

    @property
    def sqrmag(self):
        return reduce(lambda p, c: p+c*c, self.m)

    @property
    def magnitude(self):
        return math.sqrt(self.sqrmag)

    @property
    def normalized(self):
        return self / self.magnitude

    def norm_mag(self):
        """
        Returns tuple like (normalized, magnitude)
        """
        mag = self.magnitude
        return (self / mag, mag)

    @property
    def round(self):
        return self.c([round(e) for e in self.m])


class V2(V):
    def __init__(self, x=0, y=0, m=None):
        if m is not None:
            super().__init__(m)
        else:
            super().__init__([x, y])

    @staticmethod
    def c(m):
        return V2(m[0], m[1])

    @property
    def x(self):
        return self.m[0]

    @x.setter
    def x(self, v):
        self.m[0] = v

    @property
    def y(self):
        return self.m[1]

    @y.setter
    def y(self, v):
        self.m[1] = v


class V3(V):
    def __init__(self, x=0, y=0, z=0, m=None):
        if m is not None:
            super().__init__(m)
        else:
            super().__init__([x, y, z])

    @staticmethod
    def c(m):
        return V3(m[0], m[1], m[2])

    @property
    def x(self):
        return self.m[0]

    @x.setter
    def x(self, v):
        self.m[0] = v

    @property
    def y(self):
        return self.m[1]

    @y.setter
    def y(self, v):
        self.m[1] = v

    @property
    def z(self):
        return self.m[2]

    @z.setter
    def z(self, v):
        self.m[2] = v

    @property
    def v2(self) -> V2:
        return V2(self.x, self.y)


if __name__ == "__main__":
    """
    Test
    """
    a = V3(1, 2, 0)
    print(a == (1, 2, 0))
    print(a == (1, 2, 3))
    print(a == V2(1, 2))
    print(a == V2(1, 3))
    print(a == V3(1, 2, 0))
    print(a == V3(1, 2, 3))
    print(a != (1, 2, 0))
