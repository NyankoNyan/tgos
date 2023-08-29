from .image import Image
from .common_types import Vector2


class Sprite(object):
    __slots__ = ["image", "anchor"]

    def __init__(self,
                 image: Image,
                 anchor: Vector2 = None,
                 symbAnchor: Vector2 = None) -> None:
        assert (image != None)
        self.image = image
        if anchor is not None:
            self.anchor = anchor
        elif symbAnchor is not None:
            self.anchor = Vector2(
                symbAnchor.x/(image.size_x - 1) if image.size_x > 1 else .5,
                symbAnchor.y/(image.size_y - 1) if image.size_y > 1 else .5)
        else:
            self.anchor = Vector2(.5, .5)

    def draw(self, coord: Vector2, draw_callback):
        offset_x = -self.anchor.x * self.image.size_x
        offset_y = (1 - self.anchor.y) * self.image.size_y
        for ix in range(self.image.size_x):
            for iy in range(self.image.size_y):
                symb_info = self.image.get_char(ix, iy)
                draw_callback(
                    coord + (ix, -iy) + (offset_x, offset_y), symb_info)
