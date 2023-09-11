import math
from tgos import App, Vector2, Vector3, Sprite, SceneObject, Font, TextObject, AppContext
import tgos.color as color
import ascii_sprites.grass as grass
from ascii_sprites.bigsymb import shadow

class DemoContext(AppContext):
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


class DemoApp(App):
    def _user_update(self):
        context = self.context
        context.frame_counter += 1
        stage_val = context.frame_counter * math.pi / 18
        center = (context.scr.scr_size.x // 2, context.scr.scr_size.y // 2)
        grass_count = len(context.grass_gos)

        context.tree_go.coord = Vector3(center[0], 10, -2)

        for i in range(grass_count):
            angle = stage_val + i * math.pi * 2 / grass_count
            go = context.grass_gos[i]

            offset = Vector3(math.sin(angle) * 10, math.cos(angle) * 1.1, 0)
            offset.z = -offset.y
            go.coord = Vector3(center[0], 9, -1) + offset

        context.text.coord = Vector3(
            center[0] + math.sin(stage_val)*3, 19+math.cos(stage_val)*3, -999)


if __name__ == "__main__":
    DemoApp(DemoContext).start()
