import curses
from sceneobject import SceneObject

class AppContext:
    def __init__(self, stdscr: curses.window) -> None:
        self.stdscr = stdscr
        self.exit = False
        self.scr_resize = False
        self.scr_size = (0, 0)
        self.key = -1
        self.bg_color_buffer = []
        self.color_buffer = []
        self.symbol_buffer = []
        self.scene_objects = set()
        self._custom_init()

    def instaniate(self, scene_obj: SceneObject = SceneObject()) -> SceneObject:
        self.scene_objects.add(scene_obj)
        return scene_obj

    def _custom_init(self):
        pass
