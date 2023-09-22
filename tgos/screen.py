from __future__ import annotations
from typing import Callable

from tgos.image import SymbolInfo
from .common_types import Vector2
from . import color
import curses


curses_color_map = {
    color.WHITE: curses.COLOR_WHITE,
    color.BLACK: curses.COLOR_BLACK,
    color.BROWN: 166,
    color.GREEN: 46,
    color.RED: 196,
    color.YELLOW: 227,
    color.MAGENTA: 165,
    color.CYAN: 123,
    color.PINK: 207,
    color.BLUE: 27,
    color.GRAY: 245,
    color.DARK_GRAY: 233
}
"""
Это карта цветов. Подходит для xterm256, а у нас местами xterm8, 
а потому нужно сделать несколько таких карт и выставлять подходящую.
"""


class Screen(object):
    """Предосталяет функционал взаимодействия с экраном"""

    color_pairs = {}
    color_pairs_counter = 0

    def __init__(self) -> None:
        self.scr_size: Vector2 = Vector2(0, 0)
        self.bg_color_buffer = []
        self.color_buffer = []
        self.symbol_buffer = []
        self.flag_buffer = []

    def clear_buffers(self) -> None:
        buff_len = self.scr_size.x * self.scr_size.y
        self.symbol_buffer = [' '] * buff_len
        self.color_buffer = [color.WHITE] * buff_len
        self.bg_color_buffer = [color.BLACK] * buff_len
        self.flag_buffer = [0] * buff_len

    def __get_color_pair(self, text_color: str, bg_color: str) -> int:
        """
        Возвращает уникальный идентификатор для цветовой пары. 
        Если цветовая пара используется впервые, создаст новый идентификатор.

        Этот идентификатор использует ncurses для понимания, какой цвет символа и фона надо рисовать.
        Число цветовых пар не может быть больше 256, при это цветовая пара с индексом 0 изначально задана.
        Это ограничение на уровне C-кода ncurses, поэтому не может быть изменено.

        В теории можно инвертировать цветовую пару, что даст дополнительно ёщё 256 цветовых пар.
        Можно использовать интенсивность окраски, что увеличит число цветовых пар ещё втрое.
        """
        cur_text_color = self.__get_curses_color(text_color)
        cur_bg_color = self.__get_curses_color(bg_color)

        pair_name = str(cur_text_color) + '|' + str(cur_bg_color)

        try:
            return Screen.color_pairs[pair_name]
        except:
            Screen.color_pairs_counter += 1
            curses.init_pair(Screen.color_pairs_counter,
                             cur_text_color, cur_bg_color)
            Screen.color_pairs[pair_name] = Screen.color_pairs_counter
            return Screen.color_pairs_counter

    def draw_buffers(self, stdscr: curses.window):
        """
        Пересылает изображение из буферов в рисовалку curses. 
        """
        for ix in range(self.scr_size.x):
            for iy in range(self.scr_size.y):
                flat_coord = iy * self.scr_size.x + ix
                color_pair = self.__get_color_pair(
                    self.color_buffer[flat_coord], self.bg_color_buffer[flat_coord])
                flags = self.flag_buffer[flat_coord]
                try:
                    stdscr.addch(
                        iy, ix, self.symbol_buffer[flat_coord], curses.color_pair(color_pair) | flags)
                except:
                    pass

    def set_intense(self, scr_pos: Vector2, intense: int):
        curs_pos = self.mirror_coord(scr_pos)
        flat_coord = curs_pos.y * self.scr_size.x + curs_pos.x
        clear_mask = curses.A_LOW | curses.A_BOLD
        current = self.flag_buffer[flat_coord]
        current &= ~ clear_mask
        if intense == color.LOW_INTENSE:
            current |= curses.A_LOW
        elif intense == color.HIGH_INTENSE:
            current |= curses.A_BOLD
        self.flag_buffer[flat_coord] = current

    def __get_curses_color(self, color: str) -> str:
        "Переводит цвет из имени в движке (white, black, ...) в индексы curses (0, 1, ...)"
        try:
            return curses_color_map[color]
        except:
            return curses.COLOR_BLACK

    def mirror_coord(self, coord: Vector2) -> Vector2:
        return Vector2(coord.x, self.scr_size.y - coord.y)
    
class DrawContext(object):
    def __init__(self, screen: Screen) -> None:
        self.screen = screen

Shader = Callable[[Vector2, SymbolInfo, DrawContext], None]
DrawCallback = Callable[[Vector2, SymbolInfo, Shader, bool], None]
