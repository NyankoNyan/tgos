from __future__ import annotations
from tgos import Panel, Rect, SceneObject, Vector2, color
from tgos.ui.label import Label
from copy import deepcopy
from functools import partial
from typing import Callable


class ButtonsPanel(Panel):
    DOTPAINT = "dotpaint"
    LINEPAINT = "linepaint"
    SQUAREPAINT = "squarepaint"
    PICK = "pick"
    VSPACING = 0
    HSPACING = 1

    def __init__(self,
                 parent: SceneObject = None,
                 tool_pick_callback: Callable[[str], None] = None) -> None:
        super().__init__(rect=Rect(0, 0, 1, 1), parent=parent, rc_target=True)

        self.buttons = {
            self.DOTPAINT: "DOT",
            self.LINEPAINT: "LIN",
            self.SQUAREPAINT: "SQR",
            self.PICK: "PCK",
        }
        self.tool_pick_callback = tool_pick_callback
        self.__picked = None
        self.__color = color.WHITE
        self.__bg_color = color.BLUE
        self.__btn_instances: dict = {}

    def start(self):
        # Add buttons
        for btn_key in self.buttons:

            btn: Label = Label(
                text=self.buttons[btn_key],
                parent=self,
                rc_target=True,
                color=self.__color,
                bg_color=self.__bg_color)

            self.context.instaniate(btn)
            btn.click_callback = lambda x: self.__on_tool_pick(btn_key)

            btn.click_callback = partial(
                lambda b, x: self.__on_tool_pick(b), btn_key)
            self.__btn_instances[btn_key] = btn

    def __on_tool_pick(self, tool: str):
        if self.__picked is not None:
            btn: Label = self.__btn_instances[self.__picked]
            btn.color = self.__color
            btn.bg_color = self.__bg_color
        self.__picked = tool
        btn: Label = self.__btn_instances[tool]
        btn.color = self.__bg_color
        btn.bg_color = self.__color

        if self.tool_pick_callback is not None:
            self.tool_pick_callback(tool)

    def update_height(self) -> None:
        offsets = self.__get_buttons_offsets()
        borders = self.rect.height - self.inside.height
        self.rect.height = (max(offsets.values(), key=lambda x: x.y).y
                            + 1 + borders)

    def update_child_pos(self) -> None:
        offsets = self.__get_buttons_offsets()
        inner_rect = self.inside
        for btn_key in offsets:
            offset = offsets[btn_key]
            btn: Label = self.__btn_instances[btn_key]
            btn.rect = btn.rect.snap_to(
                inner_rect, top=offset.y, left=offset.x)

    def __get_buttons_offsets(self) -> dict[str, Vector2]:
        max_width = self.inside.width
        result = {}
        offset = Vector2()
        for btn_key in self.buttons:
            btn: Label = self.__btn_instances[btn_key]
            if btn.rect.width + offset.x > max_width and offset.x > 0:
                offset.x = 0
                offset.y += 1 + self.VSPACING
            result[btn_key] = deepcopy(offset)
            offset.x += btn.rect.width + self.HSPACING
        return result