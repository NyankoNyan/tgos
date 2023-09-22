from tgos import *
from tgos.appcontext import AppContext


class DemoContext(AppContext):
    def _custom_init(self):
        self.snow = self.instaniate(
            ParticleSystem(ch="*",
                           coord=Vector3(0, 0, 0),
                           emit_zone=RectEmitZone(
                               Rect(5, 5, 5, 5),
                               Vector2(0, -1)),
                           speed=5,
                           emit_per_sec=10,
                           p_life_time=10,
                           color=WHITE))
        self.snow2 = self.instaniate(
            ParticleSystem(ch="*",
                           coord=Vector3(0, 0, 0),
                           emit_zone=RectEmitZone(
                               Rect(5, 5, 5, 5),
                               Vector2(4, -6)),
                           speed=8,
                           emit_per_sec=3,
                           p_life_time=10,
                           color=RED))


class DemoApp(App):
    def __init__(self, context_class: AppContext) -> None:
        super().__init__(context_class, mock_mode=False)

    def _user_update(self):
        scr_size = self.context.scr.scr_size
        self.context.snow.emit_zone.rect = Rect(
            0, scr_size.y - 1, scr_size.x, 1)
        self.context.snow2.emit_zone.rect = Rect(
            0, scr_size.y - 1, scr_size.x, 1)


if __name__ == "__main__":
    DemoApp(DemoContext).start()
