import os
import curses
from . import color
import math
import time
from .appcontext import AppContext
from .common_types import Vector2
from .image import Image, SymbolInfo


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


class App(object):
    """
    Это наш основной класс приложения. Он умеет всё рисовать. Из-за этого он сложный и жирный.
    """
    color_pairs = {}
    color_pairs_counter = 0

    def __init__(self, contextClass: AppContext) -> None:
        self.contextClass = contextClass
        self.context = contextClass
        self.last_timer = time.time()
        self.framerate = 15

    def start(self):
        os.environ.setdefault("ESCDELAY", "25")
        curses.wrapper(self.__main)

    def __main(self, stdscr: curses.window):
        "Здесь происходит инициализация и деинициализация curses, а также запуск основного обработчика."
        self.context = self.contextClass(stdscr)
        curses.update_lines_cols()
        stdscr.clear()
        curses.noecho()
        stdscr.nodelay(True)
        curses.cbreak()
        curses.curs_set(False)
        curses.start_color()
        curses.use_default_colors()
        stdscr.keypad(True)
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        # print('\033[?1003h') # enable mouse tracking with the XTERM API
        stdscr.timeout(1000//self.framerate)

        self.__main_loop()

        curses.endwin()

    def __main_loop(self):
        skip_first = True

        while (True):
            context = self.context
            if skip_first:
                skip_first = False
            else:
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
        if (context.key in (27, 275)):
            context.exit = True

        self.__send_tick()
        self._user_update()

    def __send_tick(self):
        curr_timer = time.time()
        delta = curr_timer - self.last_timer
        if delta > 0:
            self.last_timer = curr_timer
            for o in list(self.context.tickable_objects):
                o.tick(delta)
        self.context.flush_remove()

    def _user_update(self):
        pass

    def __draw_all(self):
        "Рисует сцену"
        context = self.context
        self.__clear_screen_buffers()
        context.stdscr.clear()

        if context.main_camera is None:
            self.__camera_offset = Vector2()
        else:
            self.__camera_offset = context.main_camera.offset

        def draw_callback(coord: Vector2,
                          symb_info: SymbolInfo,
                          screen_space: bool = False):
            "Через вызов этой функции будет происходить отрисовка во всех объектах сцены"
            if screen_space:
                scr_coord = coord
            else:
                scr_coord = self.__camera_offset + coord
            self.__draw_symbol(
                (math.floor(scr_coord.x), math.floor(context.scr_size[1] - scr_coord.y)), symb_info)

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
        """
        Пересылает изображение из буферов в рисовалку curses. 
        """
        context = self.context
        for ix in range(context.scr_size[0]):
            for iy in range(context.scr_size[1]):
                flat_coord = iy * context.scr_size[0] + ix
                color_pair = self.__get_color_pair(
                    context.color_buffer[flat_coord], context.bg_color_buffer[flat_coord])
                try:
                    context.stdscr.addch(
                        iy, ix, context.symbol_buffer[flat_coord], curses.color_pair(color_pair))
                except:
                    pass

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
            return App.color_pairs[pair_name]
        except:
            App.color_pairs_counter += 1
            curses.init_pair(App.color_pairs_counter,
                             cur_text_color, cur_bg_color)
            App.color_pairs[pair_name] = App.color_pairs_counter
            return App.color_pairs_counter

    def __get_curses_color(self, color: str) -> str:
        "Переводит цвет из имени в движке (white, black, ...) в индексы curses (0, 1, ...)"
        try:
            return curses_color_map[color]
        except:
            return curses.COLOR_BLACK

    def __draw_game_objects(self, draw_callback):
        """
        Отрисовывает все доступные для рисования объекты сцены, предварительно сортируя их по глубине.
        Объекты, рисуемые иерархически, используют сортировку родительского объекта и рисуются поверх него.
        """
        gos = list(self.context.scene_objects)
        gos.sort(key=lambda x: x.coord.z)
        for go in gos:
            if go.active and (go.parent is None or not go.draw_in_hier):
                go.draw(draw_callback)

    def __draw_symbol(self, coord: list, symb_info: SymbolInfo) -> None:
        """
        Распихивает графический символ по буферам. 
        Если для символа установлен прозрачный фон, будет использован фон с текущей позиции вывода.

        Сивол не попадающий в границы экрана будет проигнорирован.
        """
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

    def __draw_image(self, sprite: Image, coord: list):
        for ix in range(sprite.size_x):
            for iy in range(sprite.size_y):
                symb_info = sprite.get_char(ix, iy)
                self.__draw_symbol((coord[0]+ix, coord[1]+iy), symb_info)
