"""
Camera Demo
"""
from tgos import *
from ascii_sprites.actors import sprites as hero


class DemoContext(AppContext):
    def _custom_init(self):
        self.static = self.instaniate()
        self.instaniate(
            SceneObject(sprite=hero,
                        coord=Vector3(0, 0, 0),
                        parent=self.static))


class DemoApp(App):
    pass


if __name__ == "__main__":
    DemoApp(DemoContext).start()
