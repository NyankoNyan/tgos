from ..screen import DrawCallback, Shader
from .element import Element
from ..sceneobject import SceneObject
from ..common_types import Rect
from ..sprite import Sprite


class Panel(Element):
    def __init__(self,
                 rect: Rect = Rect(1, 1, 1, 1),
                 parent: SceneObject = None,
                 rc_target: bool = True,
                 border_sprite: Sprite = None,
                 shader=None) -> None:
        super().__init__(rect=rect, parent=parent, rc_target=rc_target, shader=shader)
        self.border_spite = border_sprite

    def draw(self, draw_callback: DrawCallback) -> None:
        if self.border_spite is not None:
            self.border_spite.resize = self.rect.size
            self.border_spite.draw(
                self.glpos.v2 + self.rect.corner, draw_callback, self.shader)
        super().draw(draw_callback)

    def get_inner_rect(self, local_space) -> Rect:
        if self.border_spite is None or self.border_spite.borders is None:
            result = self.rect
        else:
            borders = self.border_spite.borders
            result = Rect(self.rect.x + borders.l,
                          self.rect.y + borders.b,
                          self.rect.width - borders.l - borders.r,
                          self.rect.height - borders.b - borders.t)
        if not local_space:
            result.corner += self.glpos.v2
        return result

    @property
    def inside(self) -> Rect:
        return self.get_inner_rect(False)

    @property
    def local_inside(self) -> Rect:
        return self.get_inner_rect(True)
