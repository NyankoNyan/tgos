import tgos.color as color
from tgos import Image, Sprite, Vector2
"""
Pallete
░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀
▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐░▒▓▔▕▖▗▘▙▚▛▜▝▞▟ 
"""
hero_color_map = {
    "1": color.BLUE
}

images = {
    "hero_r": Image(
        main_layer="""
 ╔═══╗
 ║._.║
┌╢   ╟┐
^╚╤═╤╝^
  └ └
""",
        bg_layer="""
 
  111
  111
 

""",
        color_map=hero_color_map
    ),
    "hero_l": Image(
        main_layer="""
 ╔═══╗
 ║._.║
┌╢   ╟┐
^╚╤═╤╝^
  ┘ ┘
""",
        bg_layer="""
 
  111
  111
  

""",
        color_map=hero_color_map
    ),
    "hero_atack_r": Image(
        main_layer="""
 ╔═══╗
 ║._.║
┌╢   ╟──<
^╚╤═╤╝
  └ └
""",
        bg_layer="""
 
  111
  111
 

""",
        color_map=hero_color_map
    ),
    "hero_atack_l": Image(
        main_layer="""
   ╔═══╗
   ║._.║
>──╢   ╟┐
   ╚╤═╤╝^
    ┘ ┘
""",
        bg_layer="""

    111
    111


 """,
        color_map=hero_color_map
    ),
}

sprites = {
    "hero_r": Sprite(
        image=images["hero_r"],
        symbAnchor=Vector2(4, 1)),
    "hero_l": Sprite(
        image=images["hero_l"],
        symbAnchor=Vector2(4, 1)),
    "hero_atack_r": Sprite(
        image=images["hero_atack_r"],
        symbAnchor=Vector2(4, 1)),
    "hero_atack_l": Sprite(
        image=images["hero_atack_l"],
        symbAnchor=Vector2(6, 1))
}
