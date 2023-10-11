from image_editor.buttons_panel import ButtonsPanel
from tgos import SceneObject, color


from typing import Callable


class MainModeGroup(ButtonsPanel):
    DOTPAINT = "dotpaint"
    LINEPAINT = "linepaint"
    SQUAREPAINT = "squarepaint"
    PICK = "pick"

    def __init__(self,
                 parent: SceneObject = None,
                 tool_pick_callback: Callable[[str], None] = None) -> None:
        super().__init__(parent, tool_pick_callback, click_mode=ButtonsPanel.CLICK_OPTION)
        self.buttons = {
            self.DOTPAINT: "DOT",
            self.LINEPAINT: "LIN",
            self.SQUAREPAINT: "SQR",
            self.PICK: "Pick",
        }
        self._bg_color_selected = color.GREEN
        self._color_selected = color.BLACK