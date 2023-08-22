import math
from application import App
import ascii_sprites.grass as grass
from common_types import Vector2, Vector3
from sprite import Sprite
from sceneobject import SceneObject
import color
from textobject import Font, TextObject
from ascii_sprites.bigsymb import shadow
from appcontext import AppContext


class GameContext(AppContext):
    def _custom_init(self):
        self.frame_counter = 0
        tree_sprite = Sprite(grass.tree_1, Vector2(.5, 0))
        grass_sprite = Sprite(grass.grass_1, Vector2(.5, 0))
        self.tree_go = self.instaniate(SceneObject(tree_sprite))
        self.grass_gos = [self.instaniate(
            SceneObject(grass_sprite)) for i in range(5)]
        font = Font(shadow, color=color.RED,
                    auto_bg=True, offset=Vector2(1, 2))
        self.text = self.instaniate(TextObject(font, "DEMO",
                                               Vector3(20, 10, -999)))


class GameApp(App):
    def _user_update(self):
        context = self.context
        stage_val = context.frame_counter * math.pi / 18
        # stage = math.sin(context.frame_counter * math.pi / 18)
        center = (context.scr_size[0] // 2, context.scr_size[1] // 2)
        grass_count = len(context.grass_gos)

        # context.tree_go.coord = Vector3(center[0] + int(stage * 6), 3, -2)
        context.tree_go.coord = Vector3(center[0], 10, -2)

        for i in range(grass_count):
            angle = stage_val + i * math.pi * 2 / grass_count
            # context.grass_gos[i].coord = Vector3(
            #     center[0] + (i-1) * 10 + stage * 12, 2, -1)
            go = context.grass_gos[i]

            offset = Vector3(math.sin(angle) * 10, math.cos(angle) * 1.1, 0)
            offset.z = -offset.y
            go.coord = Vector3(center[0], 9, -1) + offset

        context.text.coord = Vector3(
            center[0] + math.sin(stage_val)*3, 19+math.cos(stage_val)*3, -999)


if __name__ == "__main__":
    GameApp(GameContext).start()
