from ascii_sprites import borders
from .border_shader import border_shader
from tgos import DrawCallback, Image, Panel, Rect, Sprite, SymbolInfo, Vector2, color


class ImageWindow(Panel):
    def __init__(self) -> None:
        super().__init__(rect=Rect(0, 0, 10, 10), rc_target=True,
                         border_sprite=borders.thick, shader=border_shader)
        self.__image: Image = None
        self.__sprite: Sprite = None
        self.__selected: Vector2 = None
        self.larrow = SymbolInfo(symbol='>', color=color.RED)
        self.tarrow = SymbolInfo(symbol='v', color=color.RED)

    def draw(self, draw_callback: DrawCallback):
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
        return Rect(inner_rect.x, inner_rect.y + inner_rect.height - img_size.y, img_size.x, img_size.y)

    def start(self):
        pass

    def tick(self, delta):
        if self.click_state is not None:
            sel = self.click_state.coord
            img_rect = self.__get_image_rect()
            if (img_rect.x <= sel.x < img_rect.x + img_rect.width
                    and img_rect.y <= sel.y < img_rect.y + img_rect.height):
                self.__selected = sel - img_rect.corner
            self.click_state = None

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
