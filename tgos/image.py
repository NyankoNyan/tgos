default_color_map = {
    "0": "black",
    "1": "white"
}


class SymbolInfo(object):
    __slots__ = [
        "alpha",
        "bg_alpha",
        "symbol",
        "color",
        "bg_color"
    ]

    def __init__(self, alpha, symbol, color, bg_alpha, bg_color) -> None:
        self.alpha = alpha
        self.symbol = symbol
        self.color = color
        self.bg_alpha = bg_alpha
        self.bg_color = bg_color


class Image(object):
    __slots__ = [
        "main_layer",
        "color_layer",
        "bg_layer",
        "color_map",
        "default_color",
        "size_x",
        "size_y"
    ]

    def __init__(self,
                 size_x: int = None,
                 size_y: int = None,
                 main_layer: str = None,
                 color_layer: str = None,
                 bg_layer: str = None,
                 default_color: str = "white",
                 color_map: dict = default_color_map) -> None:

        assert (main_layer != None)

        self.main_layer = self._raw_layer_to_list(main_layer)
        self.color_layer = self._raw_layer_to_list(color_layer)
        self.bg_layer = self._raw_layer_to_list(bg_layer)
        self.color_map = color_map
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

    @staticmethod
    def _raw_layer_to_list(raw_layer: str) -> list:
        if raw_layer == None:
            return None
        else:
            return list(l.rstrip(' ') for l in raw_layer.split("\n")[1:-1])

    def _calc_x_size(self) -> int:
        return max(self._calc_layer_x_size(self.main_layer),
                   self._calc_layer_x_size(self.bg_layer),
                   self._calc_layer_x_size(self.color_layer))

    @staticmethod
    def _calc_layer_x_size(layer: list) -> int:
        max_len = 0
        if layer != None:
            for line in layer:
                max_len = max(max_len, len(line))
        return max_len

    def _calc_y_size(self) -> int:
        lens = []
        lens.append(self._calc_layer_y_size(self.main_layer))
        if self.bg_layer != None:
            lens.append(self._calc_layer_y_size(self.bg_layer))
        if self.color_layer != None:
            lens.append(self._calc_layer_y_size(self.color_layer))
        max_len = max(lens)
        min_len = min(lens)
        if max_len != min_len:
            raise Exception("Variuos layer height")
        return max_len

    @staticmethod
    def _calc_layer_y_size(layer: list) -> int:
        if layer == None:
            return 0
        else:
            return len(layer)

    def get_char(self, x: int, y: int) -> SymbolInfo:
        """
        Returns (alpha, symbol, color, bgalpha, bgcolor)
        """
        alpha = True
        color = self.default_color
        bgalpha = True
        bgcolor = self.default_color

        _, symbol = self._get_layer_char(self.main_layer, x, y)
        if symbol != ' ':
            alpha = False

        if self.color_layer != None:
            _, colorch = self._get_layer_char(self.color_layer, x, y)
            if colorch != ' ':
                color = self._map_color(colorch)
                alpha = False

        if self.bg_layer != None:
            _, colorch = self._get_layer_char(self.bg_layer, x, y)
            if colorch != ' ':
                bgcolor = self._map_color(colorch)
                bgalpha = False

        return SymbolInfo(alpha, symbol, color, bgalpha, bgcolor)

    @staticmethod
    def _get_layer_char(layer: list, x: str, y: str) -> list:
        if y < 0 or y >= len(layer):
            return (False, ' ')
        line = layer[y]
        if x < 0 or x >= len(line):
            return (False, ' ')
        return (True, line[x])

    def _map_color(self, color: str) -> str:
        try:
            return self.color_map[color]
        except:
            return self.default_color
