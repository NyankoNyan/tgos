

from tgos.common_types import Borders, Vector2
from tgos.image import Image
from tgos.sprite import Sprite


def borderify(image: Image, borders: Borders = Borders(1, 1, 1, 1)) -> Sprite:
    return Sprite(image=image, anchor=Vector2(0, 0), borders=borders)


thick = borderify(Image(main_layer="""
╔═╗
║ ║
╚═╝
"""))

thin = borderify(Image(main_layer="""
┌─┐
│ │
└─┘
"""))

flowers = borderify(borders=Borders(2, 2, 2, 2), image=Image(main_layer="""
 *   * 
*┤Oo.├*
 │   │
*┤.oO├*
 │   │
"""))

gothic = borderify(borders=Borders(1, 2, 2, 1), image=Image(main_layer="""
│││
╔~╗─
8 8─
╚~╝─
"""))
