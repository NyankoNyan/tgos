from __future__ import annotations
from typing import Callable

from tgos.screen import DrawCallback, Shader
from .image import SymbolInfo
from .sprite import Sprite
from .common_types import Vector3
import tgos.appcontext


class SceneObject(object):
    __slots__ = ["sprite", "coord", "context",
                 "__parent", "__children", "active", "draw_in_hier", "shader"]

    def __init__(self,
                 sprite: Sprite = None,
                 coord: Vector3 = Vector3(0, 0, 0),
                 parent: SceneObject = None,
                 draw_in_hier: bool = False,
                 shader: Callable[[list, SymbolInfo], None] = None) -> None:
        self.sprite = sprite
        self.coord = coord
        self.context: tgos.appcontext.AppContext = None
        self.__parent: SceneObject = None
        self.__children: list[SceneObject] = []
        self.parent = parent
        self.active = True
        self.draw_in_hier = draw_in_hier
        self.shader = shader

    def draw(self, draw_callback: DrawCallback) -> None:
        if self.sprite is not None:
            self.sprite.draw(self.glpos.v2, draw_callback, self.shader)
        self._draw_children(draw_callback)

    def _draw_children(self, draw_callback: DrawCallback) -> None:
        for ch in self.__children:
            if ch.draw_in_hier:
                ch.draw(draw_callback)

    @property
    def glpos(self):
        if self.parent is None:
            return self.coord
        else:
            return self.parent.glpos + self.coord

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, v: SceneObject):
        if self.__parent != v:
            if v is None:
                self.__parent.remove_child(self)
            else:
                v.add_child(self)

    def add_child(self, so: SceneObject):
        assert so is not None
        if so.__parent == self:
            return
        if so.__parent is not None:
            so.__parent.remove_child(so)
        self.__children.append(so)
        so.__parent = self

    def remove_child(self, so: SceneObject):
        assert so is not None
        self.__children.remove(so)
        so.__parent = None

    @property
    def children(self):
        return self.__children
