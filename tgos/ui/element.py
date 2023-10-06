from __future__ import annotations
from ..sceneobject import SceneObject
from ..common_types import Rect, Vector2, Vector3


class ClickState(object):
    def __init__(self, btn: int, event: int, coord: Vector2) -> None:
        self.btn = btn
        self.event = event
        self.coord = coord


class Element(SceneObject):
    __slots__ = ["rect", "rc_target", "click_state"]

    def __init__(self,
                 rect: Rect = Rect(0, 0, 1, 1),
                 parent: SceneObject = None,
                 rc_target: bool = True,
                 shader=None) -> None:
        super().__init__(parent=parent, draw_in_hier=True, shader=shader)
        self.rect = rect
        self.rc_target = rc_target
        self.click_state: ClickState = None

    def on_click(self) -> None:
        context = self.context
        self.click_state = ClickState(
            context.mouse_btn, context.mouse_event, context.mouse_coord - self.glpos.v2)

    def search_raycast(self, pos: Vector2) -> Element:
        for ch in self.children:
            if ch.active and isinstance(ch, Element):
                elem = ch.search_raycast(pos)
                if elem is not None:
                    return elem
        if (self.rc_target
            and self.rect.x <= pos.x - self.glpos.x < self.rect.x + self.rect.width
                and self.rect.y <= pos.y - self.glpos.y < self.rect.y + self.rect.height):
            return self
