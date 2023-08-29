from .common_types import Vector2, Vector3
from .sprite import Sprite
from .sceneobject import SceneObject
from ascii_sprites.side_tiles import platforms
from . import symbmap
"""
Pallete
░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀
"""


class TileBuilder(SceneObject):
    def __init__(self,
                 coord: Vector3 = Vector3(0, 0, 0),
                 tilemap: [str, str] = None,
                 tiles: [str, Sprite] = None,
                 cell_size: Vector2 = Vector2(1, 1)
                 ) -> None:
        super().__init__(None, coord)
        self.tilemap = symbmap.mirror_y(symbmap.raw_layer_to_list(tilemap))
        self.size = Vector2(symbmap.calc_layer_x_size(self.tilemap),
                            symbmap.calc_layer_y_size(self.tilemap))
        self.tiles = tiles
        self.cell_size = cell_size

    def start(self):
        for ix in range(self.size.x):
            for iy in range(self.size.y):
                _, symb = symbmap.get_layer_char(self.tilemap, ix, iy)
                if symb != ' ':
                    offset = Vector3(ix * self.cell_size.x,
                                     iy * self.cell_size.y, 0)
                    self.context.instaniate(
                        SceneObject(
                            sprite=self.tiles[symb],
                            coord=self.coord + offset
                        )
                    )


platforms_sprites = Sprite.sprityfy(platforms, Vector2(0.5, 0))

default_usage = TileBuilder(
    tilemap="""
┌───────┐

    
┌───────┐

┌─┐   ┌─┐
█████████
""",
    tiles={
        "┌": platforms_sprites["left"],
        "┐": platforms_sprites["right"],
        "─": platforms_sprites["center"],
        "█": platforms_sprites["level_bottom"]
    },
    cell_size=Vector2(5, 3)
)
