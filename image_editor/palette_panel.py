from __future__ import annotations
from tgos import DrawCallback, Panel, SymbolInfo, Vector2, color, mouse
from tgos.screen import DrawCallback


class PalettePanel(Panel):
    """Кусочек окна с тулзами на которой располагаются символы
    """
    HMARGIN = 0
    VMARGIN = 0
    HORIZONTAL_SPACE = 1
    VERTICAL_SPACE = 1

    def __init__(self, parent: Panel, palette: str) -> None:
        self.parent: Panel
        super().__init__(parent=parent, rc_target=True)
        self.color = color.WHITE
        self.bg_color = color.BLACK
        self.palette = palette
        self.__selected_elem = -1

    def tick(self, delta: float) -> None:
        if self.click_state is not None:
            if self.click_state.btn == mouse.LBUTTON:
                sel_index = self.__check_elem(
                    self.click_state.coord.x, self.click_state.coord.y)
                if sel_index >= 0:
                    self.__selected_elem = sel_index
            self.click_state = None

    def draw(self, draw_callback: DrawCallback) -> None:
        super().draw(draw_callback)
        self.__draw_palette(draw_callback)

    def update_height(self):
        elems_on_row = self.__get_elems_on_row()
        if self.border_spite is None:
            borders_offset = 0
        else:
            borders_offset = self.border_spite.borders.t + self.border_spite.borders.b
        self.rect.height = (self.VMARGIN * 2 + 1 + borders_offset +
                            (len(self.palette) // elems_on_row - 1) * (self.VERTICAL_SPACE + 1))

    def __draw_palette(self, draw_callback: DrawCallback) -> None:
        inner_rect = self.inside
        elems_on_row = self.__get_elems_on_row()
        for i in range(len(self.palette)):
            ch = self.palette[i]
            x, y = self.__get_elem_coord(i, elems_on_row)
            if 0 <= x - inner_rect.x < inner_rect.width and 0 <= y - inner_rect.y < inner_rect.height:
                draw_callback(
                    self.glpos.v2 + Vector2(x, y),
                    SymbolInfo(
                        symbol=ch,
                        color=self.bg_color if i == self.__selected_elem else self.color,
                        bg_color=self.color if i == self.__selected_elem else self.bg_color,
                        bg_alpha=False))

    def __get_elems_on_row(self) -> int:
        inner_rect = self.inside
        return (inner_rect.width - self.HMARGIN * 2 +
                self.HORIZONTAL_SPACE) // (self.HORIZONTAL_SPACE + 1)

    def __get_elem_coord(self, elem_index: int, elems_on_row: int) -> tuple[int, int]:
        inner_rect = self.inside
        x = (inner_rect.x + self.HMARGIN +
             (elem_index % elems_on_row) * (self.HORIZONTAL_SPACE + 1))
        y = (inner_rect.y + inner_rect.height - 1 -
             self.VMARGIN - (elem_index // elems_on_row) *
             (self.VERTICAL_SPACE + 1))
        return (x, y)

    def __check_elem(self, x: int, y: int) -> int:
        inner_rect = self.inside
        elems_on_row = self.__get_elems_on_row()
        offset_y = -(y - inner_rect.y - inner_rect.height + 1 + self.VMARGIN)
        if offset_y < 0:
            return -1
        real_y = offset_y // (self.VERTICAL_SPACE + 1)
        check_y = offset_y % (self.VERTICAL_SPACE + 1)
        if check_y != 0:
            return -1
        offset_x = x - inner_rect.x - self.HMARGIN
        if offset_x < 0:
            return -1
        real_x = offset_x // (self.HORIZONTAL_SPACE + 1)
        check_x = offset_x % (self.HORIZONTAL_SPACE + 1)
        if check_x != 0 or real_x >= elems_on_row:
            return -1
        index = elems_on_row * real_y + real_x
        if index >= len(self.palette):
            return -1
        else:
            return index

    def is_symbol_select(self) -> bool:
        return self.__selected_elem >= 0

    def get_symbol(self) -> str:
        return self.__palette[self.__selected_elem]