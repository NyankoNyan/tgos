
import curses

LBUTTON = 1
RBUTTON = 2
MBUTTON = 3

PRESS = 1
RELEASE = 2
CLICK = 3
DOUBLE_CLICK = 4
TRIPLE_CLICK = 5


def map_button(curses_code: int):
    if curses_code in (curses.BUTTON1_PRESSED,
                       curses.BUTTON1_RELEASED,
                       curses.BUTTON1_CLICKED,
                       curses.BUTTON1_DOUBLE_CLICKED,
                       curses.BUTTON1_TRIPLE_CLICKED):
        return LBUTTON
    elif curses_code in (curses.BUTTON2_PRESSED,
                         curses.BUTTON2_RELEASED,
                         curses.BUTTON2_CLICKED,
                         curses.BUTTON2_DOUBLE_CLICKED,
                         curses.BUTTON2_TRIPLE_CLICKED):
        return MBUTTON
    elif curses_code in (curses.BUTTON3_PRESSED,
                         curses.BUTTON3_RELEASED,
                         curses.BUTTON3_CLICKED,
                         curses.BUTTON3_DOUBLE_CLICKED,
                         curses.BUTTON3_TRIPLE_CLICKED):
        return RBUTTON
    else:
        return 0


def map_event(curses_code: int):
    if curses_code in (curses.BUTTON1_PRESSED,
                       curses.BUTTON2_PRESSED,
                       curses.BUTTON3_PRESSED,
                       curses.BUTTON4_PRESSED):
        return PRESS
    elif curses_code in (curses.BUTTON1_RELEASED,
                         curses.BUTTON2_RELEASED,
                         curses.BUTTON3_RELEASED,
                         curses.BUTTON4_RELEASED):
        return RELEASE
    elif curses_code in (curses.BUTTON1_CLICKED,
                         curses.BUTTON2_CLICKED,
                         curses.BUTTON3_CLICKED,
                         curses.BUTTON4_CLICKED):
        return CLICK
    elif curses_code in (curses.BUTTON1_DOUBLE_CLICKED,
                         curses.BUTTON2_DOUBLE_CLICKED,
                         curses.BUTTON3_DOUBLE_CLICKED,
                         curses.BUTTON4_DOUBLE_CLICKED):
        return DOUBLE_CLICK
    elif curses_code in (curses.BUTTON1_TRIPLE_CLICKED,
                         curses.BUTTON2_TRIPLE_CLICKED,
                         curses.BUTTON3_TRIPLE_CLICKED,
                         curses.BUTTON4_TRIPLE_CLICKED):
        return TRIPLE_CLICK
    else:
        return 0
