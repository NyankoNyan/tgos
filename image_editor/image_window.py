from typing import Callable
from ascii_sprites import borders
from .border_shader import border_shader
from tgos import DrawCallback, Image, Panel, Rect, Sprite, SymbolInfo, Vector2, color, mouse
import math


class ImageWindow(Panel):
    SYMB_PAINT_MODE = "symb"
    LINE_PAINT_MODE = "line"
    RECT_PAINT_MODE = "rect"
    PICK_MODE = "pick"

    BORDERS = borders.borderify(Image(main_layer="""
╔═╗
║.║
╚═╝
"""))

    def __init__(self) -> None:
        super().__init__(rect=Rect(0, 0, 10, 10), rc_target=True,
                         border_sprite=self.BORDERS, shader=border_shader)
        self.__image: Image = None
        self.__sprite: Sprite = None
        self.__selected: Vector2 = None
        self.__mode = None
        self.larrow = SymbolInfo(symbol='>', color=color.RED)
        self.tarrow = SymbolInfo(symbol='v', color=color.RED)
        self.pick_symb_callback: Callable[[SymbolInfo], None] = None
        self.is_draw_symb = True
        self.is_draw_color = True
        self.is_draw_bg = True
        self.is_erase = False
        self.is_erase_bg = False
        self.color = color.WHITE
        self.bg_color = color.BLACK
        self.symb = " "

    def draw(self, draw_callback: DrawCallback):
        # Draw panel with borders
        super().draw(draw_callback)
        # Draw sprite
        if self.__sprite is not None:
            inner_rect = self.inside
            top_left_corner = self.glpos.v2 + \
                (0, inner_rect.height - 1) + inner_rect.corner
            self.__sprite.draw(top_left_corner, draw_callback)
        # if self.__selected:
        #     img_rect = self.__get_image_rect()
        #     # Draw selected part
        #     self.context.scr.set_intense(
        #         self.glpos.v2 + img_rect.corner + self.__selected, color.HIGH_INTENSE)
        #     # Draw navigation arrows over borders
        #     draw_callback(self.glpos.v2 + Vector2(img_rect.x - 1,
        #                                           img_rect.y + self.__selected.y),
        #                   self.larrow)
        #     draw_callback(self.glpos.v2 + Vector2(img_rect.x + self.__selected.x,
        #                                           img_rect.y + img_rect.height),
        #                   self.tarrow)

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
            img_coord = sel - img_rect.corner
            if self.__mode == self.PICK_MODE:
                if (img_rect.x <= sel.x < img_rect.x + img_rect.width
                        and img_rect.y <= sel.y < img_rect.y + img_rect.height):
                    if self.pick_symb_callback is not None:
                        self.pick_symb_callback(self.pick_symbol(img_coord))
                    # self.__selected = sel - img_rect.corner
            elif (self.__mode == self.SYMB_PAINT_MODE
                  and self.click_state.event == mouse.CLICK):
                self.draw_symb(img_coord, self.__get_draw_symbol())
            elif self.__mode == self.LINE_PAINT_MODE:
                pass
            elif self.__mode == self.RECT_PAINT_MODE:
                pass
            self.click_state = None

    def __get_draw_symbol(self):
        return SymbolInfo(
            alpha=self.is_erase,
            symbol=self.symb,
            color=self.color,
            bg_alpha=self.is_erase_bg,
            bg_color=self.bg_color)

    def pick_symbol(self, rect_coord: Vector2) -> SymbolInfo:
        img = self.__sprite.image
        size = img.size
        if not 0 <= rect_coord.x < size.x or not 0 <= rect_coord.y < size.y:
            raise Exception()
        img_coord = self.__rect_to_img_coord(rect_coord, img)
        symb = img.get_char(img_coord.x, img_coord.y)
        return symb

    def __rect_to_img_coord(self, coord: Vector2, image: Image) -> Vector2:
        size = image.size
        return Vector2(coord.x, size.y - coord.y - 1)

    def draw_symb(self, rect_coord: Vector2, symb: SymbolInfo) -> None:
        img = self.__sprite.image
        current = self.pick_symbol(rect_coord)
        img_coord = self.__rect_to_img_coord(rect_coord, img)

        if self.is_draw_color:

            current.color = symb.color

        if self.is_draw_bg:
            current.bg_color = symb.bg_color
            current.bg_alpha = False
        elif self.is_erase_bg:
            current.bg_alpha = True

        if self.is_draw_symb:
            current.symbol = symb.symbol
            current.alpha = False
        elif self.is_erase:
            current.symbol = " "
            current.alpha = True

        img.set_char(img_coord.x, img_coord.y, current)

    def draw_square(self, rect: Rect, symb: SymbolInfo) -> None:
        for x in range(rect.width):
            for y in range(rect.height):
                self.draw_symb(Vector2(x + rect.x, y + rect.y), symb)

    def draw_line(self, coord_from: Vector2, coord_to: Vector2, symb: SymbolInfo) -> None:
        if coord_from == coord_to:
            self.draw_symb(coord_from, symb)
        else:
            delta = coord_to - coord_from
            if abs(delta.x) > abs(delta.y):
                step = math.copysign(1, delta.x)
                max_i = abs(delta.x)
                normal = delta / max_i
                for i in range(max_i + 1):
                    coord = Vector2(
                        coord_from.x + step * i,
                        coord_from.y + normal * i)
                    self.draw_symb(coord, symb)
            else:
                step = math.copysign(1, delta.y)
                max_i = abs(delta.y)
                normal = delta / max_i
                for i in range(max_i + 1):
                    coord = Vector2(
                        coord_from.x + normal * i,
                        coord_from.y + step * i)
                    self.draw_symb(coord, symb)

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, v: Image):
        self.__image = v
        self.__image.prepare_edit()
        if self.__image is None:
            self.__sprite = None
        else:
            self.__sprite = Sprite(image=self.__image, anchor=Vector2(0, 1))

    def set_mode(self, mode: str):
        self.__mode = mode
