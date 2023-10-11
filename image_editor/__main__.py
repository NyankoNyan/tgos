from __future__ import annotations
from image_editor.main_mode_group import MainModeGroup
from .status_text_window import StatusTextWindow
from .tools_window import ToolsWindow
from .image_window import ImageWindow
from tgos import *
from ascii_sprites.actors import images as hero_img

MOCK_DEBUG = False


class ImageController(object):
    def __init__(self,
                 image_window: ImageWindow,
                 tools_window: ToolsWindow,
                 status_window: StatusTextWindow) -> None:
        self.image_window = image_window
        self.tools_window = tools_window
        tools_window.symb_pick_callback = self.on_symb_pick
        tools_window.color_pick_callback = self.on_color_pick
        tools_window.bg_color_pick_callback = self.on_bg_color_pick
        tools_window.tool_pick_callback = self.on_tool_pick
        image_window.pick_symb_callback = self.on_image_symb_pick
        
        status_window.image = image_window.image

    def on_tool_pick(self, tool: str, active: bool) -> None:
        if tool == MainModeGroup.DOTPAINT:
            self.image_window.set_mode(ImageWindow.SYMB_PAINT_MODE)
        elif tool == MainModeGroup.LINEPAINT:
            self.image_window.set_mode(ImageWindow.LINE_PAINT_MODE)
        elif tool == MainModeGroup.SQUAREPAINT:
            self.image_window.set_mode(ImageWindow.RECT_PAINT_MODE)
        elif tool == MainModeGroup.PICK:
            self.image_window.set_mode(ImageWindow.PICK_MODE)

    def on_color_pick(self, color: str) -> None:
        self.image_window.color = color

    def on_bg_color_pick(self, color: str) -> None:
        self.image_window.bg_color = color

    def on_symb_pick(self, symb: str) -> None:
        self.image_window.symb = symb

    def on_image_symb_pick(self, symb: SymbolInfo) -> None:
        self.tools_window.color_panel.external_pick(symb.color)
        if not symb.bg_alpha:
            self.tools_window.bg_color_panel.external_pick(symb.bg_color)
        if not symb.alpha:
            self.tools_window.palette_panel.external_pick(symb.symbol)


class ImageEditorContext(AppContext):
    def _custom_init(self):
        self.mel = self.instaniate(MouseEventListener())
        self.imgwnd: ImageWindow = self.instaniate(ImageWindow())
        self.imgwnd.image = hero_img["hero_atack_l"]
        self.current_focus = None
        self.toolwnd: ToolsWindow = self.instaniate(ToolsWindow())
        self.statwnd: StatusTextWindow = self.instaniate(StatusTextWindow())

        self.controller = ImageController(self.imgwnd, self.toolwnd, self.statwnd)

    def set_focus(self, panel: Panel):
        if self.current_focus is not None and hasattr(self.current_focus, "on_loose_focus"):
            self.current_focus.on_loose_focus()
        self.current_focus = panel
        if self.current_focus is not None and hasattr(self.current_focus, "on_gain_focus"):
            self.current_focus.on_gain_focus()


class ImageEditorApp(App):
    CMD_WINDOW_HEIGHT = 4
    TOOL_WINDOW_WIDTH = 20

    def __init__(self, contextClass: AppContext) -> None:
        super().__init__(contextClass, mock_mode=MOCK_DEBUG)
        self.framerate = -1
        self.context: ImageEditorContext

    def _user_update(self):
        self._split_windows()

    def _split_windows(self):
        self.context.imgwnd.rect = Rect(
            0,
            self.CMD_WINDOW_HEIGHT - 1,
            self.context.scr.scr_size.x - self.TOOL_WINDOW_WIDTH + 1,
            self.context.scr.scr_size.y - self.CMD_WINDOW_HEIGHT + 1
        )
        self.context.toolwnd.rect = Rect(
            self.context.scr.scr_size.x - self.TOOL_WINDOW_WIDTH,
            self.CMD_WINDOW_HEIGHT - 1,
            self.TOOL_WINDOW_WIDTH,
            self.context.scr.scr_size.y - self.CMD_WINDOW_HEIGHT + 1
        )
        self.context.statwnd.rect = Rect(
            0,
            0,
            self.context.scr.scr_size.x,
            self.CMD_WINDOW_HEIGHT
        )

    def _user_draw(self, draw_callback):
        return


class MouseEventListener(SceneObject):
    def before_tick(self, delta):
        if (self.context.mouse_event in (mouse.CLICK, mouse.PRESS)
                and self.context.mouse_btn == mouse.LBUTTON):
            for so in self.context.scene_objects:
                if so.parent is None and isinstance(so, Element):
                    rc_so = so.search_raycast(self.context.mouse_coord)
                    if rc_so is not None:
                        rc_so.on_click()


if __name__ == "__main__":
    ImageEditorApp(ImageEditorContext).start()
