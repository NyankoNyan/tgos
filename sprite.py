from image import Image
from common_types import Vector2


class Sprite(object):
    __slots__ = ["image", "anchor"]

    def __init__(self, image: Image, anchor: Vector2 = Vector2(.5, .5)) -> None:
        assert (image != None)
        self.image = image
        self.anchor = anchor

    def draw(self, coord: Vector2, draw_callback):
        offset_x = -self.anchor.x * self.image.size_x
        offset_y = (1 - self.anchor.y) * self.image.size_y
        for ix in range(self.image.size_x):
            for iy in range(self.image.size_y):
                symb_info = self.image.get_char(ix, iy)
                draw_callback(
                    coord + (ix, -iy) + (offset_x, offset_y), symb_info)

