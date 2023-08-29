import tgos.color as color
from tgos import Image, Sprite, Vector2
"""
Pallete
░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀
▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐░▒▓▔▕▖▗▘▙▚▛▜▝▞▟ 
"""

color_map = {
    '1': color.GRAY,
    '2': color.RED
}

platforms = Image.apply(
    {
        "center": Image(
            main_layer="""

▚▚▚▚▚
▔▔▔▔▔
""",
            color_layer="""

22222
11111
""",
            bg_layer="""
11111


"""
        ),
        "left": Image(
            main_layer="""
▗
▐ ▚▚▚
▝▔▔▔▔
""",
            color_layer="""
1
12222
11111
""",
            bg_layer="""
 1111


"""
        ),
        "right": Image(
            main_layer="""
    ▖
▚▚▚ ▌
▔▔▔▔▘
""",
            color_layer="""
    1
22221
11111
""",
            bg_layer="""
1111


"""
        ),
        "level_bottom": Image(
            main_layer="""
▓▓▓▓▓
▒▒▒▒▒
░░░░░
""",
            color_layer="""
11111
11111
11111
"""
        )
    },
    color_map=color_map)
