from ..image import SymbolInfo
from .element import Element
from ..common_types import Vector2, Rect
from ..sceneobject import SceneObject
from .. import color


class Label(Element):
    def __init__(self,
                 text: str = "",
                 pos: Vector2 = Vector2(0, 0),
                 parent: SceneObject = None,
                 rc_target: bool = False,
                 color: str = color.WHITE,
                 bg_color: str = None) -> None:
        rect = Rect(pos.x, pos.y, len(text), 1)
        super().__init__(rect=rect, parent=parent, rc_target=rc_target)
        self.__text = text
        self.color = color
        self.bg_color = bg_color

    def draw(self, draw_callback):
        for i, ch in enumerate(self.__text):
            if self.bg_color is not None:
                si = SymbolInfo(symbol=ch,
                                color=self.color,
                                bg_alpha=False,
                                bg_color=self.bg_color)
            else:
                si = SymbolInfo(symbol=ch,
                                color=self.color)
            draw_callback(self.glpos + (i, 0), si, True)
        super().draw(draw_callback)

    def on_click(self):
        pass

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, v):
        self.__text = v
        self.rect.width = len(v)
