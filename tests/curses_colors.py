import curses


def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    try:
        for i in range(0, 256):
            curses.init_pair(i, i, 0)
            # stdscr.addstr(" COL ", curses.color_pair(i) | curses.A_REVERSE | curses.A_BLINK)
            stdscr.addstr(str(i).center(5), curses.color_pair(i) 
                          | curses.A_REVERSE)
    except:
        # End of screen reached
        pass
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
