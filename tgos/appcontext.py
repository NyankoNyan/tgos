import curses

from .camera import Camera
from .sceneobject import SceneObject


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
        self.scene_objects: set[SceneObject] = set()
        self.tickable_objects = set()
        self.remove_queue = set()
        self.main_camera: Camera = None
        self._custom_init()

    def instaniate(self, scene_obj: SceneObject = SceneObject()) -> SceneObject:
        self.scene_objects.add(scene_obj)
        scene_obj.context = self
        if self.__is_tickable(scene_obj):
            self.tickable_objects.add(scene_obj)
        if hasattr(scene_obj, "start"):
            scene_obj.start()
        return scene_obj

    def destroy(self, scene_obj: SceneObject) -> None:
        self.remove_queue.add(scene_obj)

    def flush_remove(self):
        for o in self.remove_queue:
            self.scene_objects.remove(o)
            if self.__is_tickable(o):
                self.tickable_objects.remove(o)
        self.remove_queue.clear()

    def _custom_init(self):
        pass

    def __is_tickable(self, obj):
        return hasattr(obj, "tick")
