from tgos import *
import random


class DemoContext(AppContext):
    def _custom_init(self):
        self.salute = self.instaniate(self.__get_ps())
        self.salute.color = RED
        self.salute.emit_zone.angle_limit = Vector2(
            math.radians(20), math.radians(70))
        self.salute2 = self.instaniate(self.__get_ps())
        self.salute2.color = YELLOW
        self.salute2.emit_zone.angle_limit = Vector2(
            math.radians(110), math.radians(160))

    def __get_ps(self):
        return ParticleSystem(
            ch=".",
            coord=Vector3(0, 0, 0),
            emit_zone=RoundEmitZone(
                center=Vector2(5, 5),
                radius=2,
                ellipse_mod=Vector2(1, 0.5)
            ),
            speed=Vector2(15, 30),
            gravity=Vector2(0, -8),
            emit_per_sec=0,
            life_time=5,
            emit_actions=[
                EmitAction(.1, 20)
            ],
            circle_length=3)


class DemoApp(App):
    def _user_update(self):
        pos = Vector2(self.context.scr_size[0]/2,
                      self.context.scr_size[1]/2)
        self.context.salute.emit_zone.center = pos - Vector2(20, 0)
        self.context.salute2.emit_zone.center = pos + Vector2(20, 0)


if __name__ == "__main__":
    DemoApp(DemoContext).start()
