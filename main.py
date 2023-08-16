import curses
import time


def main(stdscr: curses.window):
    curses.update_lines_cols()
    stdscr.clear()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)
    stdscr.keypad(True)

    stdscr.addstr(5, 20, "Pretty text")
    stdscr.border()
    stdscr.refresh()
    time.sleep(3)

    curses.endwin()


def game_loop():
    pass


if __name__ == "__main__":
    curses.wrapper(main)
