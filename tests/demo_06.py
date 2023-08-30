"""
Camera Demo
"""
from tgos import *
from ascii_sprites.actors import sprites as hero
import curses


class MovableCamera(Camera):
    MOVE_DIST = Vector2(5, 2)

    def tick(self, delta: float):
        if self.context.key == curses.KEY_LEFT:
            self.coord.x -= self.MOVE_DIST.x
        elif self.context.key == curses.KEY_RIGHT:
            self.coord.x += self.MOVE_DIST.x
        elif self.context.key == curses.KEY_UP:
            self.coord.y += self.MOVE_DIST.y
        elif self.context.key == curses.KEY_DOWN:
            self.coord.y -= self.MOVE_DIST.y


class DemoContext(AppContext):
    def _custom_init(self):
        self.static = self.instaniate()
        self.instaniate(
            SceneObject(sprite=hero["hero_l"],
                        coord=Vector3(0, 0, 0),
                        parent=self.static))
        self.main_camera = self.instaniate(MovableCamera())


class DemoApp(App):
    pass


if __name__ == "__main__":
    DemoApp(DemoContext).start()
