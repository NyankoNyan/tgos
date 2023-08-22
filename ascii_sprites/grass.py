from image import Image
import color

grass_1 = Image(
    size_x=5,
    size_y=2,
    main_layer=r"""
\ | /
 \|/
""",
    color_layer="""
1 1 1
 111
""",
    color_map={
        "1": color.GREEN
    }
)

tree_1 = Image(
    main_layer=r"""
    (   )
  (  ( )  )
(   (   )   )
  (  ( )  )
    | | |
    | | |
    | | |
   /  |  \
""",
    bg_layer="""
    ggggg
  ggggggggg
ggggggggggggg
  ggggggggg
    bbbbb
    bbbbb
    bbbbb
   bbbbbbb
""",
    color_map={
        "g": color.GREEN,
        "b": color.BROWN
    },
    default_color=color.BLACK
)
