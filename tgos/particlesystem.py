from __future__ import annotations
import math
import random

from tgos.common_types import Vector2
from .sceneobject import SceneObject
from .common_types import Rect, Vector2, Vector3
from . import color
from .image import SymbolInfo
from . import support


class Particle(object):
    __slots__ = ["coord", "death_time", "active", "speed"]

    def __init__(self,
                 coord=None,
                 active=False,
                 death_time=0,
                 speed=Vector2(0, 0)) -> None:
        self.coord = coord
        self.death_time = death_time
        self.active = active
        self.speed = speed


class EmitAction(object):
    __slots__ = ["time", "count"]

    def __init__(self, time: float, count: int) -> None:
        self.time = time
        self.count = count


class EmitZone(object):
    def get_emit(self) -> (Vector2, Vector2):
        raise Exception()


class RectEmitZone(EmitZone):
    def __init__(self, rect: Rect, dir: Vector2) -> None:
        self.rect = rect
        self.dir = dir.normalized

    def get_emit(self) -> (Vector2, Vector2):
        return (self.__get_emit_coord(), self.dir)

    def __get_emit_coord(self) -> Vector2:
        return Vector2(random.randrange(self.rect.width) + self.rect.x,
                       random.randrange(self.rect.height) + self.rect.y)


class RoundEmitZone(EmitZone):
    def __init__(self,
                 center: Vector2,
                 radius: float = 0,
                 ellipse_mod: Vector2 = Vector2(1, 1),
                 angle_limit: Vector2 = None) -> None:
        self.center = center
        self.radius = radius
        self.ellipse_mod = ellipse_mod
        self.angle_limit = angle_limit

    def get_emit(self) -> (Vector2, Vector2):
        if self.angle_limit is None:
            angle = random.random() * math.pi * 2
        else:
            l = self.angle_limit
            angle = random.random() * (l.y-l.x) + l.x
        distance = random.random() * self.radius
        dir = Vector2(math.cos(angle) * self.ellipse_mod.x,
                      math.sin(angle) * self.ellipse_mod.y)
        pos = dir * distance
        return (self.center + pos, dir)


class ParticleSystem(SceneObject):
    def __init__(self,
                 ch: str,
                 emit_zone: EmitZone,
                 coord: Vector3 = Vector3(0, 0, 0),
                 life_time: float = 1,
                 emit_per_sec: float = 10,
                 speed=1,
                 color: str = color.WHITE,
                 gravity: Vector2 = Vector2(0, 0),
                 emit_actions: list[EmitAction] = None,
                 circle_length: float = 5) -> None:
        super().__init__(coord=coord)

        self.ch = ch
        self.emit_zone = emit_zone
        self.life_time = life_time
        self.emit_per_sec = emit_per_sec
        self.speed = speed
        self.color = color
        self.gravity = gravity
        self.emit_actions = emit_actions
        self.circle_length = circle_length

        self.__time = 0
        self.__time_consume = 0
        self.__circle_time = 0
        # self.__emit_delta = 1 / self.emit_per_sec
        default_size = self.emit_per_sec * self.life_time
        self.__particles = [Particle() for _ in range(default_size)]

    def tick(self, delta: float) -> None:
        self.__time += delta
        self.__time_consume += delta
        self.__circle_time += delta
        self.__destroy_old()
        self.__move(delta)
        self.__emit(delta)
        if self.__circle_time > self.circle_length:
            self.__circle_time = 0

    def __destroy_old(self):
        for p in self.__particles:
            if p.active and p.death_time <= self.__time:
                p.active = False

    def __move(self, delta: float):
        for p in self.__particles:
            if p.active:
                p.speed += self.gravity*delta
                p.coord += p.speed*delta

    def __emit(self, delta: float):
        if self.emit_per_sec > 0:
            emit_delta = 1 / self.emit_per_sec
            count = math.trunc(self.__time_consume / emit_delta)
            if count > 0:
                self.__time_consume -= emit_delta*count
                self.__emit_count(count)
        if self.emit_actions != None:
            for ea in self.emit_actions:
                if (self.__circle_time-delta) <= ea.time <= self.__circle_time:
                    self.__emit_count(ea.count)

    def __emit_count(self, count: int):
        if count > 0:
            free_srch = 0
            size = len(self.__particles)
            for i in range(count):
                fnd = None
                while (free_srch < size):
                    curr = self.__particles[free_srch]
                    if not curr.active:
                        fnd = curr
                        break
                    free_srch += 1
                if fnd == None:
                    fnd = Particle()
                    self.__particles.append(fnd)
                fnd.active = True
                fnd.coord, dir = self.emit_zone.get_emit()
                fnd.speed = dir * support.evaluate(self.speed)
                fnd.death_time = self.__time + self.life_time

    def draw(self, draw_callback) -> None:
        for p in self.__particles:
            if p.active:
                smb = SymbolInfo(symbol="*", color=self.color)
                pos = Vector2(p.coord.x + self.coord.x,
                              p.coord.y + self.coord.y)
                draw_callback(pos, smb)
