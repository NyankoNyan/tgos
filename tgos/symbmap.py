from __future__ import annotations


def raw_layer_to_list(raw_layer: str) -> list:
    if raw_layer == None:
        return None
    else:
        return list(l.rstrip(' ') for l in raw_layer.split("\n")[1:-1])


def mirror_y(layer: list):
    return layer[::-1]


def calc_layer_x_size(layer: list) -> int:
    max_len = 0
    if layer != None:
        for line in layer:
            max_len = max(max_len, len(line))
    return max_len


def calc_layer_y_size(layer: list) -> int:
    if layer == None:
        return 0
    else:
        return len(layer)


def get_layer_char(layer: list, x: str, y: str) -> list[bool, str]:
    if y < 0 or y >= len(layer):
        return (False, ' ')
    line = layer[y]
    if x < 0 or x >= len(line):
        return (False, ' ')
    return (True, line[x])


def set_layer_char(layer: list, x: str, y: str, value: str) -> None:
    if y < 0 or y >= len(layer):
        return
    line: str = layer[y]
    if x < 0 or x >= len(line):
        return
    layer[y] = line[:x] + value + line[x+1:]
