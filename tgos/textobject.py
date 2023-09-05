from .common_types import Vector2, Vector3
from .sceneobject import SceneObject
from .sprite import Sprite
from .image import Image
from . import color


class Font(object):
    def __init__(self,
                 sprites: dict,
                 offset: Vector2 = Vector2(1, 2),
                 color: str = color.WHITE,
                 auto_bg: bool = False) -> None:
        self.sprites = sprites
        self.offset = offset
        self.color = color
        self.auto_bg = auto_bg


class TextObject(SceneObject):

    __slots__ = ["font", "value", "anchor"]

    def __init__(self,
                 font: Font,
                 value: str,
                 coord: Vector3 = Vector3(0, 0, 0),
                 anchor: Vector2 = Vector2(.5, .5)) -> None:
        super().__init__(coord=coord)
        self.font = font
        self.value = value
        self.anchor = anchor

    def draw(self, draw_callback):
        # Callculate output size
        size = Vector2(0, 0)
        for ch in self.value:
            try:
                image = self.font.sprites[ch.upper()]
            except:
                continue
            size.x += image.size_x + self.font.offset.x
            size.y = max(size.y, image.size_y)

        offset = Vector2(size.x * -self.anchor.x,
                         size.y * (1-self.anchor.y))

        curr_offset = Vector2(0, 0)
        for ch in self.value:
            try:
                image = self.font.sprites[ch.upper()]
            except:
                continue
            self._draw_letter(image, offset + curr_offset, draw_callback)
            curr_offset.x += image.size_x + self.font.offset.x

    def _draw_letter(self, image: Image, offset: Vector2, draw_callback):
        pos = self.glpos
        for ix in range(image.size_x):
            for iy in range(image.size_y):
                symb_info = image.get_char(ix, iy)
                symb_info.color = self.font.color
                if self.font.auto_bg and symb_info.symbol == '█':
                    symb_info.bg_alpha = False
                    symb_info.bg_color = symb_info.color
                draw_callback(
                    pos + (offset.x+ix, offset.y-iy, 0), symb_info)
