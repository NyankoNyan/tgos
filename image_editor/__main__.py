from __future__ import annotations
import curses
from tgos import *
from ascii_sprites import borders
from tgos.appcontext import AppContext
from tgos.common_types import Rect
from ascii_sprites.actors import images as hero_img


class ClickState(object):
    def __init__(self, btn: int, event: int, coord: Vector2) -> None:
        self.btn = btn
        self.event = event
        self.coord = coord


class ImageWindow(Panel):
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect, rc_target=True, border_sprite=borders.thick)
        self.__image: Image = None
        self.__sprite: Sprite = None
        self.__click_state: ClickState = None
        self.__selected: Vector2 = None
        self.larrow = SymbolInfo(symbol='>', color=color.RED)
        self.tarrow = SymbolInfo(symbol='v', color=color.RED)

    def draw(self, draw_callback):
        # Draw panel with borders
        super().draw(draw_callback)
        # Draw sprite
        if self.__sprite is not None:
            inner_rect = self.inside
            top_left_corner = self.glpos.v2 + \
                (0, inner_rect.height - 1) + inner_rect.corner
            self.__sprite.draw(top_left_corner, draw_callback)
        if self.__selected:
            img_rect = self.__get_image_rect()
            # Draw selected part
            self.context.scr.set_intense(
                self.glpos.v2 + img_rect.corner + self.__selected, color.HIGH_INTENSE)
            # Draw navigation arrows over borders
            draw_callback(self.glpos.v2 + Vector2(img_rect.x - 1,
                                                  img_rect.y + self.__selected.y),
                          self.larrow)
            draw_callback(self.glpos.v2 + Vector2(img_rect.x + self.__selected.x,
                                                  img_rect.y + img_rect.height),
                          self.tarrow)

    def __get_image_rect(self) -> Rect:
        inner_rect = self.inside
        img_size = self.__sprite.image.size
        return Rect(inner_rect.x, inner_rect.height - img_size.y + 1, img_size.x, img_size.y)

    def start(self):
        pass

    def tick(self, delta):
        self.context.imgwnd.rect.width = self.context.scr.scr_size.x
        self.context.imgwnd.rect.height = self.context.scr.scr_size.y
        if self.__click_state is not None:
            sel = self.__click_state.coord
            img_rect = self.__get_image_rect()
            if (img_rect.x <= sel.x < img_rect.x + img_rect.width
                    and img_rect.y <= sel.y < img_rect.y + img_rect.height):
                self.__selected = sel - img_rect.corner
            self.__click_state = None

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

    def on_click(self):
        context = self.context
        self.__click_state = ClickState(
            context.mouse_btn, context.mouse_event, context.mouse_coord - self.glpos.v2)


class ImageEditorContext(AppContext):
    def _custom_init(self):
        self.mel = self.instaniate(MouseEventListener())
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
        self.context.imgwnd.rect.width = self.context.scr.scr_size.x
        self.context.imgwnd.rect.height = self.context.scr.scr_size.y

    def _user_draw(self, draw_callback):
        return


class MouseEventListener(SceneObject):
    def before_tick(self, delta):
        if (self.context.mouse_event in (mouse.CLICK, mouse.PRESS)
                and self.context.mouse_btn == mouse.LBUTTON):
            for so in self.context.scene_objects:
                if so.parent is None and isinstance(so, Element):
                    rc_so = so.search_raycast(self.context.mouse_coord)
                    if rc_so is not None:
                        rc_so.on_click()


if __name__ == "__main__":
    ImageEditorApp(ImageEditorContext).start()
