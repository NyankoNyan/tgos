from .element import Element
from ..sceneobject import SceneObject
from ..common_types import Rect
from ..sprite import Sprite

class Panel(Element):
    def __init__(self,
                 rect: Rect = Rect(1, 1, 1, 1),
                 parent: SceneObject = None,
                 rc_target: bool = True,
                 border_sprite: Sprite = None) -> None:
        super().__init__(rect=rect, parent=parent, rc_target=rc_target)
        self.border_spite = border_sprite

    def draw(self, draw_callback):
        self.border_spite.resize = self.rect.size
        self.border_spite.draw(self.glpos.v2, draw_callback)
        super().draw(draw_callback)