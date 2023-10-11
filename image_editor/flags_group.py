from image_editor.buttons_panel import ButtonsPanel
from tgos import SceneObject, color


from typing import Callable


class FlagsGroup(ButtonsPanel):
    USE_BG = "Paint Back"
    USE_COLOR = "Paint Symb"
    USE_SYMB = "Print Symb"

    def __init__(self,
                 parent: SceneObject = None,
                 tool_pick_callback: Callable[[str], None] = None) -> None:
        super().__init__(parent, tool_pick_callback, click_mode=ButtonsPanel.CLICK_FLAG)
        self.buttons = {
            self.USE_BG: self.USE_BG,
            self.USE_COLOR: self.USE_COLOR,
            self.USE_SYMB: self.USE_SYMB
        }
        self._bg_color = color.DARK_GRAY
        self._bg_color_selected = color.GREEN
        self._color_selected = color.BLACK