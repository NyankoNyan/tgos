import curses
import time
import os
import math
import ascii_sprites.grass as grass
from image import Image

curses_color_map = {
    "white": curses.COLOR_WHITE,
    "black": curses.COLOR_BLACK,
    "brown": 52,
    "green": 28
}

color_pairs = {}
color_pairs_counter = 0

def main(stdscr: curses.window):
    curses.update_lines_cols()
    stdscr.clear()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)
    curses.start_color()
    curses.use_default_colors()
    # curses.init_pair(1, 1, -1)
    stdscr.keypad(True)
    stdscr.timeout(100)

    game_loop(GameContext(stdscr))

    curses.endwin()


class GameContext:
    def __init__(self, stdscr: curses.window) -> None:
        self.stdscr = stdscr
        self.exit = False
        self.key = -1
        self.bg_color_buffer = []
        self.color_buffer = []
        self.symbol_buffer = []
        self._custom_init()

    def _custom_init(self):
        self.frame_counter = 0
        self.tree = grass.tree_1
        self.grass = grass.grass_1


def game_loop(context: GameContext):
    while (True):
        context.key = context.stdscr.getch()
        update_all(context)
        if (context.exit):
            break
        draw_all(context)


def update_all(context: GameContext):
    context.frame_counter += 1
    if (context.key in (27, 275)):
        context.exit = True


def draw_all(context: GameContext):
    # context.stdscr.addstr(5, 20, str(context.frame_counter))
    # context.stdscr.addstr(7, 20, str(context.key))
    context.stdscr.clear()
    stage = math.sin(context.frame_counter * math.pi / 18)
    rows, cols = context.stdscr.getmaxyx()
    center = (cols // 2, rows // 2)
    draw_sprite(context.stdscr, context.tree,
                (center[0] + int(stage * 6) - 5, center[1]))
    for i in range(3):
        draw_sprite(context.stdscr, context.grass,
                    (int(center[0] + (i-1) * 10 + stage * 12 - 5), center[1]+8))
    # draw_sprite(context.stdscr, context.test_sprite, context.test_sprite_coord)
    context.stdscr.border()
    context.stdscr.refresh()


def draw_sprite(stdscr: curses.window, sprite: Image, coord: list):
    for ix in range(sprite.size_x):
        for iy in range(sprite.size_y):
            symb_info = sprite.get_char(ix, iy)
            if not symb_info.alpha or not symb_info.bg_alpha:
                color_pair = get_color_pair(
                    symb_info.color, symb_info.bg_color, symb_info.alpha, symb_info.bg_alpha)
                try:
                    stdscr.addstr(coord[1]+iy, coord[0]+ix,
                                  symb_info.symbol, curses.color_pair(color_pair))
                except:
                    pass


def get_color_pair(text_color: str, bg_color: str, text_alpha: bool, bg_alpha: bool):

    global color_pairs_counter
    global color_pairs

    if text_alpha:
        cur_text_color = get_curses_color("white")
    else:
        cur_text_color = get_curses_color(text_color)

    if bg_alpha:
        cur_bg_color = -1
    else:
        cur_bg_color = get_curses_color(bg_color)

    pair_name = str(cur_text_color) + '|' + str(cur_bg_color)

    try:
        return color_pairs[pair_name]
    except:
        color_pairs_counter += 1
        curses.init_pair(color_pairs_counter, cur_text_color, cur_bg_color)
        color_pairs[pair_name] = color_pairs_counter
        return color_pairs_counter


def get_curses_color(color: str) -> str:
    try:
        return curses_color_map[color]
    except:
        return curses.COLOR_BLACK


if __name__ == "__main__":
    os.environ.setdefault("ESCDELAY", "25")
    curses.wrapper(main)
