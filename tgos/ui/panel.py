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

    def draw(self, draw_callback) -> None:
        if self.border_spite is not None:
            self.border_spite.resize = self.rect.size
            self.border_spite.draw(self.glpos.v2, draw_callback)
        super().draw(draw_callback)

    @property
    def inside(self) -> Rect:
        if self.border_spite is None or self.border_spite.borders is None:
            return self.rect
        else:
            borders = self.border_spite.borders
            return Rect(borders.l, borders.b,
                        self.rect.width - borders.l - borders.r,
                        self.rect.height - borders.b - borders.t)
