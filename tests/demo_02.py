from tgos import *


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
                           life_time=10,
                           color=WHITE))
        self.snow2 = self.instaniate(
            ParticleSystem(ch="*",
                           coord=Vector3(0, 0, 0),
                           emit_zone=RectEmitZone(
                               Rect(5, 5, 5, 5),
                               Vector2(4, -6)),
                           speed=8,
                           emit_per_sec=3,
                           life_time=10,
                           color=RED))


class DemoApp(App):
    def _user_update(self):
        self.context.snow.emit_zone.rect = Rect(
            0, self.context.scr_size[1] - 1, self.context.scr_size[0], 1)
        self.context.snow2.emit_zone.rect = Rect(
            0, self.context.scr_size[1] - 1, self.context.scr_size[0], 1)


if __name__ == "__main__":
    DemoApp(DemoContext).start()
