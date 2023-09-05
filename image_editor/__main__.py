from __future__ import annotations
import curses
from tgos import *
from ascii_sprites import borders
from tgos.appcontext import AppContext
from tgos.common_types import Rect
from ascii_sprites.actors import images as hero_img


class ImageWindow(Panel):
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect, rc_target=True, border_sprite=borders.thick)
        self.__image: Image = None
        self.__sprite: Sprite = None

    def draw(self, draw_callback):
        super().draw(draw_callback)
        if self.__sprite is not None:
            inner_rect = self.inside
            self.__sprite.draw(self.glpos.v2 + (0, inner_rect.height - 1) + inner_rect.corner,
                               draw_callback)

    def start(self):
        pass

    def tick(self, delta):
        self.context.imgwnd.rect.width = self.context.scr_size[0]
        self.context.imgwnd.rect.height = self.context.scr_size[1]

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, v):
        self.__image = v
        if self.__image is None:
            self.__sprite = None
        else:
            self.__sprite = Sprite(image=self.__image, anchor=Vector2(0, 1))


class ImageEditorContext(AppContext):
    def _custom_init(self):
        self.imgwnd = self.instaniate(ImageWindow(Rect(0, 1, 10, 10)))
        self.imgwnd.image = hero_img["hero_atack_l"]

        # self.text_panel = self.instaniate(
        #     Panel(rect=Rect(6, 6, 30, 10),
        #           border_sprite=borders.thick))
        # self.test_text = self.instaniate(
        #     Label(text="Test text",
        #           pos=Vector2(5, 9),
        #           bg_color=color.RED,
        #           parent=self.text_panel))
        # self.sub_panel = self.instaniate(
        #     Panel(rect=Rect(2, 1, 26, 8),
        #           border_sprite=borders.flowers,
        #           parent=self.text_panel))


class ImageEditorApp(App):
    def __init__(self, contextClass: AppContext) -> None:
        super().__init__(contextClass)
        self.framerate = -1

    def _user_update(self):
        self.context.imgwnd.rect.width = self.context.scr_size[0]
        self.context.imgwnd.rect.height = self.context.scr_size[1]

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
