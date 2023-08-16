import curses


def main(stdscr: curses.window):
    stdscr.clear()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.endwin()


if __name__ == "__main__":
    curses.wrapper(main)
