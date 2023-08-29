import tgos.color as color
from tgos import Image, Sprite, Vector2
"""
Pallete
░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀
▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐░▒▓▔▕▖▗▘▙▚▛▜▝▞▟ 
"""

magic_missile = Image(
    main_layer="""
#
""",
    color_layer="""
1
""",
    bg_layer="""
2
""",
    color_map={
        '1': color.RED,
        '2': color.YELLOW
    }
)
