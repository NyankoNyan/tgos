from __future__ import annotations
import curses
from image_editor.palette_panel import PalettePanel
from image_editor.border_shader import border_shader
from image_editor.image_window import ImageWindow
from tgos import *
from ascii_sprites import borders
from tgos.appcontext import AppContext
from tgos.common_types import Rect
from ascii_sprites.actors import images as hero_img
from tgos.sceneobject import SceneObject
from tgos.screen import DrawCallback

MOCK_DEBUG = False


class ToolsWindow(Panel):
    HPADDING = 1
    VPADDING = 0
    HORIZONTAL_SPACE = 1
    VERTICAL_SPACE = 1

    def __init__(self) -> None:
        super().__init__(rect=Rect(0, 0, 10, 10), rc_target=True,
                         border_sprite=borders.thick, shader=border_shader)
        self.__palette = "░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐▔▕▖▗▘▙▚▛▜▝▞▟"
        self.palette_panel: PalettePanel = None

    def draw(self, draw_callback: DrawCallback) -> None:
        super().draw(draw_callback)

    def _draw_children(self, draw_callback: DrawCallback) -> None:
        inner_rect = self.inside
        self.palette_panel.rect = self.palette_panel.rect.snap_to(
            inner_rect, left=self.HPADDING, right=self.HPADDING)
        self.palette_panel.update_height()
        self.palette_panel.rect = self.palette_panel.rect.snap_to(
            inner_rect, top=self.VPADDING)
        self.palette_panel.draw(draw_callback)

    def tick(self, delta: float) -> None:
        if self.click_state is not None:
            if self.click_state.btn == mouse.LBUTTON:
                pass
            self.click_state = None

    def is_symbol_select(self) -> bool:
        return self.palette_panel.is_symbol_select()

    def get_symbol(self) -> str:
        return self.palette_panel.get_symbol()

    def start(self):
        self.palette_panel = self.context.instaniate(
            PalettePanel(self, self.__palette))


class ColorPickPanel(Panel):
    def __init__(self, parent: SceneObject = None, caption: str = "") -> None:
        super().__init__(rect=Rect(1, 1, 1, 3), parent=parent, rc_target=True)
        self.__caption_text = caption
        self.__caption_obj: Label = None

    def tick(self, delta: float) -> None:
        if self.click_state is not None:
            self.click_state = None

    def start(self):
        self.__caption_obj = self.context.instaniate(
            Label(text=self.__caption, parent=self))

    def draw(self, draw_callback: DrawCallback) -> None:
        super().draw(draw_callback)


class TextCommandWindow(Panel):
    SYMB = range(0x20, 0x7f)

    def __init__(self) -> None:
        super().__init__(rect=Rect(0, 0, 10, 10), rc_target=True,
                         border_sprite=borders.thick, shader=border_shader)
        self.__focused = False
        self.__text_line: Label = None
        self.__text = ""

    def start(self) -> None:
        self.__text_line = self.context.instaniate(
            Label(pos=Vector2(1, 1), parent=self))

    def on_click(self) -> None:
        self.context.set_focus(self)

    def on_loose_focus(self) -> None:
        self.__focused = False

    def on_gain_focus(self) -> None:
        self.__focused = True

    def tick(self, delta: float) -> None:
        if self.__focused:
            if self.context.key in self.SYMB:
                self.__text = self.__text.join(self.context.key)
            elif self.context.key == curses.KEY_BACKSPACE:
                if len(self.__text) > 0:
                    self.__text = self.__text[:-2]
            elif self.context.key == curses.KEY_EXIT:
                self.__text = ""
            self.__text_line.text = self.__text


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
