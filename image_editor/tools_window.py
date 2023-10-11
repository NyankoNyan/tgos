from __future__ import annotations
from typing import Callable
from ascii_sprites import borders
from .buttons_panel import ButtonsPanel
from .color_pick_panel import ColorPickPanel
from .border_shader import border_shader
from .palette_panel import PalettePanel
from tgos import DrawCallback, Panel, Rect, color, mouse


class ToolsWindow(Panel):
    HPADDING = 1
    VPADDING = 0
    HORIZONTAL_SPACE = 1
    VERTICAL_SPACE = 1
    SPACING = 1

    def __init__(self,
                 color_pick_callback: Callable[[str], None] = None,
                 bg_color_pick_callback: Callable[[str], None] = None,
                 symb_pick_callback: Callable[[str], None] = None) -> None:
        super().__init__(rect=Rect(0, 0, 10, 10),
                         rc_target=True,
                         border_sprite=borders.thick,
                         shader=border_shader)
        self.__palette = "░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐▔▕▖▗▘▙▚▛▜▝▞▟"
        self.palette_panel: PalettePanel = None
        self.color_panel: ColorPickPanel = None
        self.bg_color_panel: ColorPickPanel = None
        self.buttons_group: ButtonsPanel = None
        self.color_pick_callback = color_pick_callback
        self.bg_color_pick_callback = bg_color_pick_callback
        self.symb_pick_callback = symb_pick_callback

    def draw(self, draw_callback: DrawCallback) -> None:
        super().draw(draw_callback)

    def __group_vecrtical(self, elements: list):
        inner_rect = self.inside
        offset = self.VPADDING

        for elem in elements:
            elem.rect = elem.rect.snap_to(
                inner_rect, left=self.HPADDING, right=self.HPADDING)
            if hasattr(elem, "update_height"):
                elem.update_height()
            elem.rect = elem.rect.snap_to(inner_rect, top=offset)
            if hasattr(elem, "update_child_pos"):
                elem.update_child_pos()

            offset += elem.rect.height + self.SPACING

    def __update_children(self):
        self.__group_vecrtical([self.buttons_group,
                                self.palette_panel,
                                self.color_panel,
                                self.bg_color_panel])

    def _draw_children(self, draw_callback: DrawCallback) -> None:
        self.__update_children()
        self.palette_panel.draw(draw_callback)
        self.color_panel.draw(draw_callback)
        self.bg_color_panel.draw(draw_callback)
        self.buttons_group.draw(draw_callback)

    def tick(self, delta: float) -> None:
        if self.click_state is not None:
            if self.click_state.btn == mouse.LBUTTON:
                pass
            self.click_state = None
        # self.__update_children()

    def is_symbol_select(self) -> bool:
        return self.palette_panel.is_symbol_select()

    def get_symbol(self) -> str:
        return self.palette_panel.get_symbol()

    def start(self):
        self.palette_panel = self.context.instaniate(
            PalettePanel(self, self.__palette,
                         lambda x: self.__on_symb_pick(x))
        )
        self.color_panel = self.context.instaniate(
            ColorPickPanel(self, "Color:",
                           lambda x: self.__on_color_pick(x))
        )
        self.bg_color_panel = self.context.instaniate(
            ColorPickPanel(self, "Background:",
                           lambda x: self.__on_bg_color_pick(x))
        )
        self.buttons_group = self.context.instaniate(
            ButtonsPanel(self, lambda x: self.__on_tool_pick(x))
        )
        self.color_panel.external_pick(color.WHITE)
        self.bg_color_panel.external_pick(color.BLACK)

    def __on_color_pick(self, color: str) -> None:
        self.palette_panel.color = color
        if self.color_pick_callback is not None:
            self.color_pick_callback(color)

    def __on_bg_color_pick(self, color: str) -> None:
        self.palette_panel.bg_color = color
        if self.bg_color_pick_callback is not None:
            self.bg_color_pick_callback(color)

    def __on_symb_pick(self, symb: str) -> None:
        if self.symb_pick_callback is not None:
            self.symb_pick_callback(symb)

    def __on_tool_pick(self, tool: str) -> None:
        pass
