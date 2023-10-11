from typing import Callable
from tgos import DrawCallback, Label, Panel, Rect, SceneObject, color, Vector2, SymbolInfo


class ColorPickPanel(Panel):
    COLORS_MARGIN_TOP = 1

    def __init__(self,
                 parent: SceneObject = None,
                 caption: str = "",
                 pick_callback: Callable[[str], None] = None) -> None:
        super().__init__(rect=Rect(1, 1, 1, 3), parent=parent, rc_target=True)
        self.__caption_text = caption
        self.__caption_obj: Label = None
        self.__selected = -1
        self.pick_callback = pick_callback
        self.colors = [
            color.WHITE,
            color.BLACK,
            color.GRAY,
            color.BLUE,
            color.RED,
            color.GREEN,
            color.BROWN,
            color.MAGENTA,
            color.PINK,
            color.CYAN,
            color.YELLOW
        ]

    def external_pick(self, color: str) -> None:
        self.__selected = self.colors.index(color)
        if self.pick_callback is not None:
            self.pick_callback(color)

    def tick(self, delta: float) -> None:
        if self.click_state is not None:
            sel_index = self.__locate_index(self.click_state.coord)
            if sel_index >= 0:
                self.__selected = sel_index
                if self.pick_callback is not None:
                    self.pick_callback(self.colors[sel_index])
            self.click_state = None

    def update_child_pos(self) -> None:
        self.__caption_obj.rect = self.__caption_obj.rect.snap_to(
            self.inside, top=0, left=0)

    def start(self):
        self.__caption_obj = self.context.instaniate(
            Label(text=self.__caption_text, parent=self))

    def draw(self, draw_callback: DrawCallback) -> None:
        super().draw(draw_callback)
        self.__draw_colors(draw_callback)

    def __elems_on_row(self) -> int:
        return self.inside.width

    def __draw_colors(self, draw_callback: DrawCallback) -> None:
        elems_on_row = self.__elems_on_row()
        inner_rect = self.inside
        for i in range(len(self.colors)):
            c = self.colors[i]
            y = inner_rect.y + inner_rect.height - 1 - \
                i // elems_on_row - self.COLORS_MARGIN_TOP
            x = inner_rect.x + i % elems_on_row
            symb = SymbolInfo(bg_alpha=False, bg_color=c)
            if self.__selected == i:
                symb.symbol = "X"
                if c == color.WHITE:
                    symb.color = color.BLACK
                else:
                    symb.color = color.WHITE
            draw_callback(Vector2(x, y) + self.glpos.v2, symb)

    def update_height(self) -> None:
        elems_on_row = self.__elems_on_row()
        self.rect.height = self.rect.height - \
            self.inside.height + \
            len(self.colors) // elems_on_row + 1 + self.COLORS_MARGIN_TOP

    def __locate_index(self, click_coord: Vector2) -> int:
        elems_on_row = self.__elems_on_row()
        inner_rect = self.inside
        x = click_coord.x - inner_rect.x
        y = inner_rect.y - click_coord.y + inner_rect.height - 1 - self.COLORS_MARGIN_TOP
        index = y * elems_on_row + x
        if (0 <= x < elems_on_row
            and 0 <= y <= len(self.colors) // elems_on_row
                and index < len(self.colors)):
            return index
        else:
            return -1
