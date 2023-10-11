from __future__ import annotations
from . import color
from . import symbmap
from .common_types import Vector2

default_color_map = {
    "0": color.BLACK,
    "1": color.WHITE
}


class SymbolInfo(object):
    "Полное описание графического символа для вывода в терминал"
    __slots__ = [
        "alpha",
        "bg_alpha",
        "symbol",
        "color",
        "bg_color"
    ]

    def __init__(self,
                 alpha=False,
                 symbol=' ',
                 color=color.WHITE,
                 bg_alpha=True,
                 bg_color=color.BLACK) -> None:
        self.alpha = alpha
        self.symbol = symbol
        self.color = color
        self.bg_alpha = bg_alpha
        self.bg_color = bg_color


class Image(object):
    """ASCII картинка.

    Разбита на несколько слоёв: символы, цвета символов, цвета фона. 
    Первая и последная строка каждого слоя не используется.
    Можете вставить в них комментарии, что угодно.
    Количество строк в слоях должно быть одинаковым.

    Цветовые слои используют символы цветов. 
    Мэппинг символов на цвета движка осуществляется через словарь color_map.
    color_map можно менять в рантайме, чтобы сменить цветовую палитру.
    """
    __slots__ = [
        "main_layer",
        "color_layer",
        "bg_layer",
        "color_map",
        "reverse_color_map",
        "default_color",
        "size_x",
        "size_y"
    ]

    COLOR_SYMB_DEF = "0123456789qwertyuiopasdfghjklzxcvbnm"

    def __init__(self,
                 size_x: int = None,
                 size_y: int = None,
                 main_layer: str = None,
                 color_layer: str = None,
                 bg_layer: str = None,
                 default_color: str = "white",
                 color_map: dict = default_color_map) -> None:

        assert (main_layer != None)

        self.main_layer = symbmap.raw_layer_to_list(main_layer)
        self.color_layer = symbmap.raw_layer_to_list(color_layer)
        self.bg_layer = symbmap.raw_layer_to_list(bg_layer)
        self.color_map = color_map
        self.reverse_color_map = {color_map[x]: x for x in color_map}
        self.default_color = default_color

        calculated_size_x = self._calc_x_size()
        calculated_size_y = self._calc_y_size()

        if size_x == None:
            self.size_x = calculated_size_x
        else:
            if calculated_size_x > size_x:
                raise Exception(
                    "Real image width bigger than parameter size_x")
            self.size_x = size_x

        if size_y == None:
            self.size_y = calculated_size_y
        else:
            if (calculated_size_y > size_y):
                raise Exception(
                    "Real image height bigger than paramter size_y")
            self.size_y = size_y

        assert (self.size_x > 0)
        assert (self.size_y > 0)

    def _calc_x_size(self) -> int:
        "Вычисляет макимальную ширину среди всех слоёв"
        return max(symbmap.calc_layer_x_size(self.main_layer),
                   symbmap.calc_layer_x_size(self.bg_layer),
                   symbmap.calc_layer_x_size(self.color_layer))

    def _calc_y_size(self) -> int:
        "Вычисляет высоту слоёв. Заодно проверяет, что высота у всех слоёв одинаковая."
        lens = []
        lens.append(symbmap.calc_layer_y_size(self.main_layer))
        if self.bg_layer != None:
            lens.append(symbmap.calc_layer_y_size(self.bg_layer))
        if self.color_layer != None:
            lens.append(symbmap.calc_layer_y_size(self.color_layer))
        max_len = max(lens)
        min_len = min(lens)
        if max_len != min_len:
            raise Exception("Variuos layer height")
        return max_len

    def get_char(self, x: int, y: int) -> SymbolInfo:
        """
        Возвращает информацию о графическом символе картинки по координате
        """
        alpha = True
        color = self.default_color
        bgalpha = True
        bgcolor = self.default_color

        _, symbol = symbmap.get_layer_char(self.main_layer, x, y)
        if symbol != ' ':
            alpha = False

        if self.color_layer != None:
            _, colorch = symbmap.get_layer_char(self.color_layer, x, y)
            if colorch != ' ':
                color = self._map_color(colorch)
                alpha = False

        if self.bg_layer != None:
            _, colorch = symbmap.get_layer_char(self.bg_layer, x, y)
            if colorch != ' ':
                bgcolor = self._map_color(colorch)
                bgalpha = False

        return SymbolInfo(alpha, symbol, color, bgalpha, bgcolor)

    def set_char(self, x: int, y: int, info: SymbolInfo):
        if info.alpha:
            symbmap.set_layer_char(self.main_layer, x, y, ' ')
        else:
            symbmap.set_layer_char(self.main_layer, x, y, info.symbol)

        if info.bg_alpha:
            symbmap.set_layer_char(self.bg_layer, x, y, ' ')
        else:
            symbmap.set_layer_char(self.bg_layer, x, y,
                                   self._map_color_reverse(info.bg_color))

        symbmap.set_layer_char(self.color_layer, x, y,
                               self._map_color_reverse(info.color))

    def _map_color(self, color: str) -> str:
        "Возвращает цвет движка по его символу. Если символ не известен, вернёт цвет по-умолчанию."
        try:
            return self.color_map[color]
        except:
            return self.default_color

    def _map_color_reverse(self, color: str) -> str:
        try:
            return self.reverse_color_map[color]
        except:
            new_color = ' '
            for ch in self.COLOR_SYMB_DEF:
                try:
                    _ = self.color_map[ch]
                except:
                    self.color_map[ch] = color
                    self.reverse_color_map[color] = ch
                    new_color = ch
                    break
            return new_color

    @staticmethod
    def apply(imgs: [str, 'Image'], color_map: [str, str] = None) -> [str, 'Image']:
        "Применяет модификаторы к словарю из изображений. Для массового изменения."
        for _, img in imgs.items():
            if color_map is not None:
                img.color_map = color_map
        return imgs

    @property
    def size(self):
        return Vector2(self.size_x, self.size_y)

    def prepare_edit(self):
        if self.bg_layer is None:
            self.bg_layer = self.__empty_color_layer()
        if self.color_layer is None:
            self.color_layer = self.__empty_color_layer()

        self.__prepare_layer_width(self.color_layer, self.size.x)
        self.__prepare_layer_width(self.bg_layer, self.size.x)

    def __empty_color_layer(self, fill: str = ' '):
        layer = []
        for y in range(self.size.y):
            layer.append(fill*self.size.x)
        return layer

    def __prepare_layer_width(self, layer: list, width: int, fill: str = ' ') -> None:
        for y in range(len(layer)):
            line = layer[y]
            curr_width = len(line)
            if curr_width < width:
                layer[y] = line + fill * (width-curr_width)
