from __future__ import annotations
import curses
from tgos import *
from ascii_sprites import borders


class ImageEditorContext(AppContext):
    def _custom_init(self):

        self.text_panel = self.instaniate(
            Panel(rect=Rect(6, 6, 30, 10),
                  border_sprite=borders.thick))
        self.test_text = self.instaniate(
            Label(text="Test text",
                  pos=Vector2(5, 9),
                  bg_color=color.RED,
                  parent=self.text_panel))
        self.sub_panel = self.instaniate(
            Panel(rect=Rect(2, 1, 26, 8),
                  border_sprite=borders.flowers,
                  parent=self.text_panel))


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
