from tgos.common_types import Vector2, Vector3
from tgos.sceneobject import SceneObject
from tgos.sprite import Sprite
from .sceneobject import SceneObject


class Camera(SceneObject):
    def __init__(self,
                 coord: Vector3 = Vector3(0, 0, 0),
                 parent: SceneObject = None,
                 pivot: Vector2 = Vector2(.5, .5)) -> None:
        super().__init__(sprite=None, coord=coord, parent=parent)
        self.pivot = pivot

    @property
    def offset(self) -> Vector2:
        return self.glpos + Vector2(self.context.scr_size.x * self.pivot.x,
                                    self.context.scr_size.y * self.pivot.y)
