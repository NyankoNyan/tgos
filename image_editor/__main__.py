from __future__ import annotations
import curses
from tgos import *
from tgos import Rect, SceneObject


default_border = Image(
    main_layer="""
╔═╗
║ ║
╚═╝
"""
)


class Element(SceneObject):
    __slots__ = ["rect", "rc_target"]

    def __init__(self,
                 rect: Rect = Rect(1, 1, 1, 1),
                 parent: SceneObject = None,
                 rc_target: bool = True) -> None:
        super().__init__(parent=parent)
        self.rect = rect
        self.rc_target = rc_target

    def draw(self, draw_callback):
        pass

    def on_click(self):
        pass

    def search_elem(self, pos: Vector2):
        for ch in self.__children:
            if ch.active and issubclass(ch, Element):
                elem = ch.search_elem(pos)
                if elem is not None:
                    return elem
        if (self.rc_target
            and self.rect.x <= pos.x < self.rect.x + self.rect.width
                and self.rect.y <= pos.y < self.rect.y + self.rect.height):
            return self


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
            draw_callback(Vector2(self.rect.x + i, self.rect.y), si, True)

    def on_click(self):
        pass

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, v):
        self.__text = v
        self.rect.width = len(v)


class ImageEditorContext(AppContext):
    def _custom_init(self):
        self.test_text = self.instaniate(
            Label(text="Test text", pos=Vector2(5, 5), bg_color=color.RED)
        )


class ImageEditorApp(App):
    def _user_draw(self, draw_callback):
        if self.context.key != -1:
            if self.context.key == curses.KEY_MOUSE:
                _, x, y, _, state = curses.getmouse()
                y = self.context.scr_size[1] - y

                draw_callback(
                    Vector2(x, y),
                    SymbolInfo(symbol=str(state)),
                    True)


if __name__ == "__main__":
    ImageEditorApp(ImageEditorContext).start()
