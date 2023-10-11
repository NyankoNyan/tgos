from ascii_sprites import borders
from .border_shader import border_shader
from tgos import Label, Panel, Rect, Vector2


import curses


class TextCommandWindow(Panel):
    SYMB = range(0x20, 0x7f)

    def __init__(self) -> None:
        super().__init__(rect=Rect(0, 0, 10, 10), rc_target=True,
                         border_sprite=borders.thick, shader=border_shader)
        self.__focused = False
        self.__text_line: Label = None
        self.__text = ""

    def start(self) -> None:
        self.__text_line = self.context.instaniate(
            Label(pos=Vector2(1, 1), parent=self))

    def on_click(self) -> None:
        self.context.set_focus(self)

    def on_loose_focus(self) -> None:
        self.__focused = False

    def on_gain_focus(self) -> None:
        self.__focused = True

    def tick(self, delta: float) -> None:
        if self.__focused:
            if self.context.key in self.SYMB:
                self.__text = self.__text.join(self.context.key)
            elif self.context.key == curses.KEY_BACKSPACE:
                if len(self.__text) > 0:
                    self.__text = self.__text[:-2]
            elif self.context.key == curses.KEY_EXIT:
                self.__text = ""
            self.__text_line.text = self.__text
