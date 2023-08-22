import os
import curses
from . import color
import math
from .appcontext import AppContext
from .common_types import Vector2
from .image import Image, SymbolInfo

curses_color_map = {
    color.WHITE: curses.COLOR_WHITE,
    color.BLACK: curses.COLOR_BLACK,
    color.BROWN: 52,
    color.GREEN: 28,
    color.RED: 1
}


class App(object):
    color_pairs = {}
    color_pairs_counter = 0

    def __init__(self, contextClass: AppContext) -> None:
        self.contextClass = contextClass
        self.context = contextClass

    def start(self):        
        os.environ.setdefault("ESCDELAY", "25")
        curses.wrapper(self.__main)

    def __main(self, stdscr: curses.window):
        self.context = self.contextClass(stdscr)
        curses.update_lines_cols()
        stdscr.clear()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)
        curses.start_color()
        curses.use_default_colors()
        # curses.init_pair(1, 1, -1)
        stdscr.keypad(True)
        stdscr.timeout(1000//15)

        self.__main_loop()

        curses.endwin()

    def __main_loop(self):
        while (True):
            context = self.context
            context.key = context.stdscr.getch()
            rows, cols = context.stdscr.getmaxyx()
            context.scr_resize = (
                context.scr_size[0] != cols or context.scr_size[1] != rows)
            if context.scr_resize:
                context.scr_size = (cols, rows)

            self.__update_all()
            if (context.exit):
                break
            self.__draw_all()

    def __update_all(self):
        context = self.context
        context.frame_counter += 1
        if (context.key in (27, 275)):
            context.exit = True

        self._user_update()

    def _user_update(self):
        pass

    def __draw_all(self):
        context = self.context
        self.__clear_screen_buffers()
        context.stdscr.clear()

        def draw_callback(coord: Vector2, symb_info: SymbolInfo):
            self.__draw_symbol(
                (math.floor(coord.x), math.floor(context.scr_size[1] - coord.y)), symb_info)

        self.__draw_game_objects(draw_callback)
        self._user_draw(draw_callback)

        self.__draw_screen_buffers()
        # context.stdscr.border()
        context.stdscr.refresh()

    def _user_draw(self, draw_callback):
        pass

    def __clear_screen_buffers(self):
        context = self.context
        buff_len = context.scr_size[0] * context.scr_size[1]
        context.symbol_buffer = [' '] * buff_len
        context.color_buffer = [color.WHITE] * buff_len
        context.bg_color_buffer = [color.BLACK] * buff_len

    def __draw_screen_buffers(self):
        context = self.context
        for ix in range(context.scr_size[0]):
            for iy in range(context.scr_size[1]):
                flat_coord = iy * context.scr_size[0] + ix
                color_pair = self.__get_color_pair(
                    context.color_buffer[flat_coord], context.bg_color_buffer[flat_coord])
                try:
                    context.stdscr.addstr(
                        iy, ix, context.symbol_buffer[flat_coord], curses.color_pair(color_pair))
                except:
                    pass

    def __get_color_pair(self, text_color: str, bg_color: str) -> int:
        cur_text_color = self.__get_curses_color(text_color)
        cur_bg_color = self.__get_curses_color(bg_color)

        pair_name = str(cur_text_color) + '|' + str(cur_bg_color)

        try:
            return App.color_pairs[pair_name]
        except:
            App.color_pairs_counter += 1
            curses.init_pair(App.color_pairs_counter,
                             cur_text_color, cur_bg_color)
            App.color_pairs[pair_name] = App.color_pairs_counter
            return App.color_pairs_counter

    def __get_curses_color(self, color: str) -> str:
        try:
            return curses_color_map[color]
        except:
            return curses.COLOR_BLACK

    def __draw_game_objects(self, draw_callback):
        gos = list(self.context.scene_objects)
        gos.sort(key=lambda x: x.coord.z)
        for go in gos:
            go.draw(draw_callback)

    def __draw_symbol(self, coord: list, symb_info: SymbolInfo) -> None:
        context = self.context

        if symb_info.bg_alpha and (symb_info.alpha or symb_info.symbol == ' '):
            return

        if not (0 <= coord[0] < context.scr_size[0]
                and 0 <= coord[1] < context.scr_size[1]):
            return

        flat_coord = coord[1] * context.scr_size[0] + coord[0]

        if symb_info.alpha:
            color = context.bg_color_buffer[flat_coord]
        else:
            color = symb_info.color

        context.color_buffer[flat_coord] = color

        if not symb_info.bg_alpha:
            bg_color = symb_info.bg_color
            context.bg_color_buffer[flat_coord] = bg_color

        context.symbol_buffer[flat_coord] = symb_info.symbol

    def __draw_sprite(self, sprite: Image, coord: list):
        for ix in range(sprite.size_x):
            for iy in range(sprite.size_y):
                symb_info = sprite.get_char(ix, iy)
                self.__draw_symbol((coord[0]+ix, coord[1]+iy), symb_info)
