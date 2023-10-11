from __future__ import annotations
from tgos import Panel, Rect, SceneObject, Vector2, color
from tgos.ui.label import Label
from copy import deepcopy
from functools import partial
from typing import Callable


class ButtonsPanel(Panel):
    __slots__ = ["buttons", "tool_pick_callback",
                 "__picked", "_color", "_bg_color", "__btn_instances",
                 "__click_mode", "__active"]

    CLICK_SIGNAL = 0
    CLICK_OPTION = 1
    CLICK_FLAG = 2

    VSPACING = 0
    HSPACING = 1

    def __init__(self,
                 parent: SceneObject = None,
                 tool_pick_callback: Callable[[str, bool], None] = None,
                 click_mode: int = 0) -> None:
        super().__init__(rect=Rect(0, 0, 1, 1), parent=parent, rc_target=True)

        self.buttons: dict[str, str] = {}
        self.tool_pick_callback = tool_pick_callback
        self.__picked = None
        self.__active: dict[str, bool] = {}
        self._color = color.WHITE
        self._bg_color = color.BLUE
        self._color_selected = color.BLUE
        self._bg_color_selected = color.WHITE
        self.__btn_instances: dict = {}
        self.__click_mode = click_mode

    def start(self):
        # Add buttons
        for btn_key in self.buttons:

            btn: Label = Label(
                text=self.buttons[btn_key],
                parent=self,
                rc_target=True,
                color=self._color,
                bg_color=self._bg_color)

            self.context.instaniate(btn)
            btn.click_callback = lambda x: self.__on_tool_pick(btn_key)

            btn.click_callback = partial(
                lambda b, x: self.__on_tool_pick(b), btn_key)
            self.__btn_instances[btn_key] = btn

    def __on_tool_pick(self, tool: str):
        if self.__click_mode == self.CLICK_OPTION:

            if self.__picked is not None:
                btn: Label = self.__btn_instances[self.__picked]
                btn.color = self._color
                btn.bg_color = self._bg_color
            self.__picked = tool
            btn: Label = self.__btn_instances[tool]
            btn.color = self._color_selected
            btn.bg_color = self._bg_color_selected

            if self.tool_pick_callback is not None:
                self.tool_pick_callback(tool, True)

        elif self.__click_mode == self.CLICK_FLAG:

            try:
                self.__active[tool] = not self.__active[tool]
            except:
                self.__active[tool] = True
            btn: Label = self.__btn_instances[tool]
            if self.__active[tool]:
                btn.color = self._color_selected
                btn.bg_color = self._bg_color_selected
            else:
                btn.color = self._color
                btn.bg_color = self._bg_color

            if self.tool_pick_callback is not None:
                self.tool_pick_callback(tool, self.__active[tool])
        else:
            if self.tool_pick_callback is not None:
                self.tool_pick_callback(tool, True)

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
