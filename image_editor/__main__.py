from __future__ import annotations
from .text_command_window import TextCommandWindow
from .tools_window import ToolsWindow
from .image_window import ImageWindow
from tgos import *
from ascii_sprites.actors import images as hero_img

MOCK_DEBUG = False


class ImageEditorContext(AppContext):
    def _custom_init(self):
        self.mel = self.instaniate(MouseEventListener())
        self.imgwnd: ImageWindow = self.instaniate(ImageWindow())
        self.imgwnd.image = hero_img["hero_atack_l"]
        self.current_focus = None
        self.toolwnd: ToolsWindow = self.instaniate(ToolsWindow())
        self.cmdwnd: TextCommandWindow = self.instaniate(TextCommandWindow())

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
        # self.context.imgwnd.rect = Rect(
        #     10,
        #     0,
        #     self.context.scr.scr_size.x-10,
        #     self.context.scr.scr_size.y-5
        # )
        self.context.toolwnd.rect = Rect(
            self.context.scr.scr_size.x - self.TOOL_WINDOW_WIDTH,
            self.CMD_WINDOW_HEIGHT - 1,
            self.TOOL_WINDOW_WIDTH,
            self.context.scr.scr_size.y - self.CMD_WINDOW_HEIGHT + 1
        )
        self.context.cmdwnd.rect = Rect(
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
