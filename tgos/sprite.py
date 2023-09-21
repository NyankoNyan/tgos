from __future__ import annotations
import math
from .image import Image
from .common_types import Borders, Rect, Vector2


class Sprite(object):
    __slots__ = ["image", "anchor", "symbAnchor",
                 "borders", "__resize", "size"]

    def __init__(self,
                 image: Image,
                 anchor: Vector2 = Vector2(.5, .5),
                 symbAnchor: Vector2 = None,
                 borders: Borders = None,
                 resize: Vector2 = None) -> None:
        assert (image != None)
        self.image = image
        self.symbAnchor = symbAnchor
        self.borders = borders
        self.__resize = resize
        self.anchor = anchor
        self.size: Vector2 = None

        self.__recalc_anchor_size()

    def __recalc_anchor_size(self) -> None:
        symbAnchor = self.symbAnchor
        image = self.image

        if self.__resize is None:
            size = Vector2(image.size_x, image.size_y)
        else:
            size = self.__resize

        if symbAnchor is not None:
            self.anchor = Vector2(
                (symbAnchor.x - 1)/(size.x - 1) if size.x > 1 else .5,
                (symbAnchor.y - 1)/(size.y - 1) if size.y > 1 else .5)
        self.size = size

    def draw(self, coord: Vector2, draw_callback) -> None:
        offset_x = -self.anchor.x * (self.size.x - 1)
        offset_y = (1 - self.anchor.y) * (self.size.y - 1)
        for ix in range(self.size.x):
            for iy in range(self.size.y):
                img_ofs = self.__get_image_offset(ix, iy)
                symb_info = self.image.get_char(img_ofs.x, img_ofs.y)
                draw_callback(
                    coord + (ix, 1-iy) + (offset_x, offset_y), symb_info)

    def __get_image_offset(self, x: int, y: int) -> Vector2:

        if self.borders is not None:
            if x < self.borders.l:
                img_x = x
            elif x >= self.size.x - self.borders.r:
                img_x = self.image.size_x - (self.size.x - x)
            else:
                cx_size = self.size.x - self.borders.l - self.borders.r
                cx_img_size = self.image.size_x - self.borders.l - self.borders.r
                img_x = (self.borders.l +
                         math.floor(cx_img_size/cx_size * (x - self.borders.l)))

            if y < self.borders.t:
                img_y = y
            elif y >= self.size.y - self.borders.b:
                img_y = self.image.size_y - (self.size.y - y)
            else:
                cy_size = self.size.y - self.borders.b - self.borders.t
                cy_img_size = self.image.size_y - self.borders.b - self.borders.t
                img_y = (self.borders.t +
                         math.floor(cy_img_size/cy_size * (y - self.borders.t)))
        else:
            img_x = math.floor(self.image.size_x / self.size.x * x)
            img_y = math.floor(self.image.size_y / self.size.y * y)

        return Vector2(img_x, img_y)

    @staticmethod
    def sprityfy(images: [str, Image],
                 anchor: Vector2 = Vector2(.5, .5)
                 ) -> [str, 'Sprite']:
        return {id: Sprite(img, anchor) for id, img in images.items()}

    @property
    def resize(self):
        return self.__resize

    @resize.setter
    def resize(self, v):
        self.__resize = v
        self.__recalc_anchor_size()
