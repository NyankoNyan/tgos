from __future__ import absolute_import
from tgos import *
import ascii_sprites.actors as actors
import ascii_sprites.bullets as bullets
import ascii_sprites.side_tiles as side_tiles
from tgos.common_types import Vector3
from tgos.sprite import Sprite
import curses
from tgos.tilebuilder import default_usage as test_tiles


class Hero(SceneObject):
    LEFT = 0
    RIGHT = 1

    STAND = 0
    ATACK = 1

    ATACK_TIME = 0.3
    STEP_LENGTH = 3
    MISSILE_R_OFFSET = Vector3(5, 2, 0)
    MISSILE_L_OFFSET = Vector3(-5, 2, 0)

    def __init__(self, coord: Vector3 = ...) -> None:
        super().__init__(None, coord)
        self.side = self.LEFT
        self.action = self.STAND
        self.atack_sequence = False
        self.atack_timer = 0
        self.__set_sprite()

    def tick(self, delta: float):
        if not self.atack_sequence:
            if self.context.key == curses.KEY_LEFT:
                self.side = self.LEFT
                self.coord.x -= self.STEP_LENGTH
                self.__set_sprite()
            elif self.context.key == curses.KEY_RIGHT:
                self.side = self.RIGHT
                self.coord.x += self.STEP_LENGTH
                self.__set_sprite()
            elif self.context.key == ord(' '):
                if not self.atack_sequence:
                    self.__start_atack()
        self.__process_atack(delta)

    def __start_atack(self):
        if not self.atack_sequence:
            self.atack_sequence = True
            self.atack_timer = 0
            self.action = self.ATACK
            self.__set_sprite()

            if self.side == self.RIGHT:
                missile_coord = self.coord + self.MISSILE_R_OFFSET
                dir = Vector3(1, 0, 0)
            else:
                missile_coord = self.coord + self.MISSILE_L_OFFSET
                dir = Vector3(-1, 0, 0)
            self.context.instaniate(Bullet(missile_coord, dir))

    def __process_atack(self, delta: float):
        if self.atack_sequence:
            self.atack_timer += delta
            if self.atack_timer >= self.ATACK_TIME:
                self.atack_sequence = False
                self.action = self.STAND
                self.__set_sprite()

    def __set_sprite(self):
        if self.action == self.ATACK:
            if self.side == self.LEFT:
                self.sprite = actors.sprites["hero_atack_l"]
            else:
                self.sprite = actors.sprites["hero_atack_r"]
        else:
            if self.side == self.LEFT:
                self.sprite = actors.sprites["hero_l"]
            else:
                self.sprite = actors.sprites["hero_r"]


class Bullet(SceneObject):

    S_MISSILE = Sprite(bullets.magic_missile)
    SPEED = 10
    LIFETIME = 3

    def __init__(self, coord: Vector3, dir: Vector3) -> None:
        super().__init__(self.S_MISSILE, coord)
        self.speed = dir * self.SPEED
        self.remain = self.LIFETIME

    def tick(self, delta: float):
        self.coord += self.speed * delta
        self.remain -= delta
        if self.remain <= 0:
            self.context.destroy(self)
            self.__create_boom()

    def __create_boom(self):
        self.context.instaniate(ParticleSystem(
            ch="*",
            emit_zone=RoundEmitZone(),
            coord=self.coord,
            color=color.YELLOW,
            p_life_time=1,
            emit_per_sec=0,
            emit_actions=[EmitAction(.001, 6)],
            life_time=1,
            speed=10,
            life_end_action=LIFE_END_DESTROY
        ))


class DemoContext(AppContext):
    def _custom_init(self):
        self.hero = self.instaniate(Hero(coord=Vector3(20, 12, 1)))
        # platforms = Sprite.sprityfy(side_tiles.platforms, Vector2(.5, 0))
        # n = 8
        # for i in range(n):
        #     coord = Vector3(5+i*5, 1, 0)
        #     if i == 0:
        #         sprite = platforms["left"]
        #     elif i == n-1:
        #         sprite = platforms["right"]
        #     else:
        #         sprite = platforms["center"]
        #     self.instaniate(SceneObject(sprite=sprite, coord=coord))
        test_tiles.coord = Vector3(5, 1, 0)
        self.instaniate(
            test_tiles
        )


class DemoApp(App):
    def _user_update(self):
        pass

    # def _user_draw(self, draw_callback):
    #     draw_callback(
    #         self.context.hero.coord,
    #         SymbolInfo(symbol="H")
    #     )


if __name__ == "__main__":
    DemoApp(DemoContext).start()
