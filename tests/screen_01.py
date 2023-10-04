from tgos import *
from tgos.screen import DrawCallback


class TestApp(App):
    def _user_draw(self, draw_callback: DrawCallback):
        # for x in range(2):
        #     for y in range(2):
        for x in range(self.context.scr.scr_size.x):
            for y in range(self.context.scr.scr_size.y):
                symb = str(y)[-1]
                draw_callback(Vector2(x, y), SymbolInfo(symbol=symb))


if __name__ == "__main__":
    TestApp(AppContext).start()
