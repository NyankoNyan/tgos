from tgos import *
import random


class DemoContext(AppContext):
    def _custom_init(self):
        self.salute = self.instaniate(self.__get_ps(YELLOW))
        self.salute2 = self.instaniate(self.__get_ps(RED))
        self.salute3 = self.instaniate(self.__get_ps(PINK))

    def __get_ps(self, color):
        return ParticleSystem(
            ch=".",
            coord=Vector3(0, 0, 0),
            emit_zone=RoundEmitZone(
                center=Vector2(5, 5),
                radius=5,
                ellipse_mod=Vector2(1, 0.5)
            ),
            speed=20,
            gravity=Vector2(0, -8),
            emit_per_sec=0,
            p_life_time=3,
            color=color,
            emit_actions=[
                EmitAction(.1, 10)
            ],
            circle_length=1)


class DemoApp(App):
    def _user_update(self):
        pos = Vector2(random.random()*self.context.scr.scr_size.x,
                      random.random()*self.context.scr.scr_size.y)
        self.context.salute.emit_zone.center = pos
        self.context.salute2.emit_zone.center = pos
        self.context.salute3.emit_zone.center = pos


if __name__ == "__main__":
    DemoApp(DemoContext).start()
