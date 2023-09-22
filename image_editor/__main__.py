from __future__ import annotations
import curses
from tgos import *
from ascii_sprites import borders
from tgos.appcontext import AppContext
from tgos.common_types import Rect
from ascii_sprites.actors import images as hero_img
from tgos.sceneobject import SceneObject
from tgos.sprite import Sprite

MOCK_DEBUG = False

class ClickState(object):
    def __init__(self, btn: int, event: int, coord: Vector2) -> None:
        self.btn = btn
        self.event = event
        self.coord = coord


def border_weights_calc(ch: str) -> list[int, int, int, int]:
    idx = [0, 0, 0, 0]
    if ch in "│┤╡╛└┴├┼╞╧╘╪┘":
        idx[0] = 1
    elif ch in "╢╣║╝╜╟╚╩╠╬╨╙╫":
        idx[0] = 2
    if ch in "└┴┬├─┼╟╨╥╙╓╫┌":
        idx[1] = 1
    elif ch in "╞╚╔╩╦╠═╬╧╤╘╒╪":
        idx[1] = 2
    if ch in "│┤╡╕┐┬├┼╞╤╒╪┌":
        idx[2] = 1
    elif ch in "╢╖╣║╗╟╔╦╠╬╥╓╫":
        idx[2] = 2
    if ch in "┤╢╖╜┐┴┬─┼╨╥╫┘":
        idx[3] = 1
    elif ch in "╡╕╣╗╝╛╩╦═╬╧╤╪":
        idx[3] = 2
    return idx


def weight_index(l: list) -> int:
    return (l[0] << 6) | (l[1] << 4) | (l[2] << 2) | l[3]


border_lines = "│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌"
border_weights = {weight_index(border_weights_calc(e)): e
                  for e in border_lines}


def border_shader(coord: Vector2, symb: SymbolInfo, context: DrawContext):
    scr = context.screen
    sb = scr.symbol_buffer
    if not (0 <= coord.x < scr.scr_size.x
            and 0 <= coord.y < scr.scr_size.y):
        return
    curr_symb = symb.symbol
    flat_coord = coord.y * scr.scr_size.x + coord.x
    if curr_symb in border_lines:
        symb2 = sb[flat_coord]
        if symb2 in border_lines:
            target_weights = [max(e[0], e[1])
                              for e in zip(border_weights_calc(curr_symb),
                                           border_weights_calc(symb2))]
            try:
                curr_symb = border_weights[weight_index(target_weights)]
            except:
                pass
    if curr_symb != " ":
        sb[flat_coord] = curr_symb
        if not symb.bg_alpha:
            scr.bg_color_buffer[flat_coord] = symb.bg_color


class ImageWindow(Panel):
    def __init__(self) -> None:
        super().__init__(rect=Rect(0, 0, 10, 10), rc_target=True, border_sprite=borders.thick, shader=border_shader)
        self.__image: Image = None
        self.__sprite: Sprite = None
        self.__click_state: ClickState = None
        self.__selected: Vector2 = None
        self.larrow = SymbolInfo(symbol='>', color=color.RED)
        self.tarrow = SymbolInfo(symbol='v', color=color.RED)

    def draw(self, draw_callback: DrawCallback):
        # Draw panel with borders
        super().draw(draw_callback)
        # Draw sprite
        if self.__sprite is not None:
            inner_rect = self.inside
            top_left_corner = self.glpos.v2 + \
                (0, inner_rect.height - 1) + inner_rect.corner
            self.__sprite.draw(top_left_corner, draw_callback)
        if self.__selected:
            img_rect = self.__get_image_rect()
            # Draw selected part
            self.context.scr.set_intense(
                self.glpos.v2 + img_rect.corner + self.__selected, color.HIGH_INTENSE)
            # Draw navigation arrows over borders
            draw_callback(self.glpos.v2 + Vector2(img_rect.x - 1,
                                                  img_rect.y + self.__selected.y),
                          self.larrow)
            draw_callback(self.glpos.v2 + Vector2(img_rect.x + self.__selected.x,
                                                  img_rect.y + img_rect.height),
                          self.tarrow)

    def __get_image_rect(self) -> Rect:
        inner_rect = self.inside
        img_size = self.__sprite.image.size
        return Rect(inner_rect.x, inner_rect.height - img_size.y + 2, img_size.x, img_size.y)

    def start(self):
        pass

    def tick(self, delta):
        if self.__click_state is not None:
            sel = self.__click_state.coord
            img_rect = self.__get_image_rect()
            if (img_rect.x <= sel.x < img_rect.x + img_rect.width
                    and img_rect.y <= sel.y < img_rect.y + img_rect.height):
                self.__selected = sel - img_rect.corner
            self.__click_state = None

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, v):
        self.__image = v
        if self.__image is None:
            self.__sprite = None
        else:
            self.__sprite = Sprite(image=self.__image, anchor=Vector2(0, 1))

    def on_click(self):
        context = self.context
        self.__click_state = ClickState(
            context.mouse_btn, context.mouse_event, context.mouse_coord - self.glpos.v2)


class ToolsWindow(Panel):
    def __init__(self) -> None:
        super().__init__(rect=Rect(0, 0, 10, 10), rc_target=True, border_sprite=borders.thick, shader=border_shader)


class TextCommandWindow(Panel):
    SYMB = range(0x20, 0x7f)

    def __init__(self) -> None:
        super().__init__(rect=Rect(0, 0, 10, 10), rc_target=True, border_sprite=borders.thick, shader=border_shader)
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

        # self.text_panel = self.instaniate(
        #     Panel(rect=Rect(6, 6, 30, 10),
        #           border_sprite=borders.thick))
        # self.test_text = self.instaniate(
        #     Label(text="Test text",
        #           pos=Vector2(5, 9),
        #           bg_color=color.RED,
        #           parent=self.text_panel))
        # self.sub_panel = self.instaniate(
        #     Panel(rect=Rect(2, 1, 26, 8),
        #           border_sprite=borders.flowers,
        #           parent=self.text_panel))


class ImageEditorApp(App):
    CMD_WINDOW_HEIGHT = 4
    TOOL_WINDOW_WIDTH = 10

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
