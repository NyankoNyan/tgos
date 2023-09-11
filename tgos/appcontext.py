import curses

from .camera import Camera
from .sceneobject import SceneObject
from .common_types import Vector2
from .screen import Screen


class AppContext:
    """
    Класс контекста. 

    Хранит в себе все используемые данные. Рекомендую добавлять пользовательские 
    данные сюда же. Что, мы зря на питоне что ли пишем. 
    А чтобы не было конфликта имён, рекомендуется называть все пользовательские атрибуты с z*
    """

    def __init__(self, stdscr: curses.window) -> None:
        self.stdscr = stdscr
        self.exit = False
        self.scr_resize = False
        # self.scr_size = (0, 0)
        self.key = -1
        # self.bg_color_buffer = []
        # self.color_buffer = []
        # self.symbol_buffer = []
        # self.flag_buffer = []
        self.scr = Screen()
        self.scene_objects: set[SceneObject] = set()
        self.tick_objects = set()
        self.before_tick_objects = set()
        self.remove_queue = set()
        self.main_camera: Camera = None
        self.mouse_btn = 0
        self.mouse_event = 0
        self.mouse_coord: Vector2 = None
        self._custom_init()

    def instaniate(self, scene_obj: SceneObject = SceneObject()) -> SceneObject:
        "Помещает объект на сцену. Возвращает этот же объект."
        self.scene_objects.add(scene_obj)
        scene_obj.context = self
        if hasattr(scene_obj, "tick"):
            self.tick_objects.add(scene_obj)
        if hasattr(scene_obj, "before_tick"):
            self.before_tick_objects.add(scene_obj)
        if hasattr(scene_obj, "start"):
            scene_obj.start()
        return scene_obj

    def destroy(self, scene_obj: SceneObject) -> None:
        "Помечает объект для удаления со сцены в конце кадра."
        self.remove_queue.add(scene_obj)

    def flush_remove(self):
        """(Не для использования)
        Вызывает удаление помещенных объектов.
        """
        for o in self.remove_queue:
            self.scene_objects.remove(o)
            if hasattr(o, "tick"):
                self.tick_objects.remove(o)
            if hasattr(o, "before_tick"):
                self.before_tick_objects.remove(o)
        self.remove_queue.clear()

    def _custom_init(self):
        "Переопределите этот метод, чтобы инициализировать свои объекты на сцене."
        pass
