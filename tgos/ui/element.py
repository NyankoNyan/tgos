from ..sceneobject import SceneObject
from ..common_types import Rect, Vector2, Vector3

class Element(SceneObject):
    __slots__ = ["rect", "rc_target"]

    def __init__(self,
                 rect: Rect = Rect(0, 0, 1, 1),
                 parent: SceneObject = None,
                 rc_target: bool = True) -> None:
        corner = rect.corner
        super().__init__(parent=parent, draw_in_hier=True,
                         coord=Vector3(corner.x, corner.y, 0))
        self.rect = rect
        self.rc_target = rc_target

    def on_click(self):
        pass

    def search_elem(self, pos: Vector2):
        for ch in self.__children:
            if ch.active and issubclass(ch, Element):
                elem = ch.search_elem(pos)
                if elem is not None:
                    return elem
        if (self.rc_target
            and self.rect.x <= pos.x < self.rect.x + self.rect.width
                and self.rect.y <= pos.y < self.rect.y + self.rect.height):
            return self