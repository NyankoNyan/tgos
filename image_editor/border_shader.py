from __future__ import annotations
from tgos import DrawContext, SymbolInfo, Vector2


def border_weights_calc(ch: str) -> list[int, int, int, int]:
    idx = [0, 0, 0, 0]
    if ch in "│┤╡╛└┴├┼╞╧╘╪┘":
        idx[0] = 1
    elif ch in "╢╣║╝╜╟╚╩╠╬╨╙╫":
        idx[0] = 2
    if ch in "└┴┬├─┼╟╨╥╙╓╫┌":
        idx[1] = 1
    elif ch in "╞╚╔╩╦╠═╬╧╤╘╒╪":
        idx[1] = 2
    if ch in "│┤╡╕┐┬├┼╞╤╒╪┌":
        idx[2] = 1
    elif ch in "╢╖╣║╗╟╔╦╠╬╥╓╫":
        idx[2] = 2
    if ch in "┤╢╖╜┐┴┬─┼╨╥╫┘":
        idx[3] = 1
    elif ch in "╡╕╣╗╝╛╩╦═╬╧╤╪":
        idx[3] = 2
    return idx


def weight_index(l: list) -> int:
    return (l[0] << 6) | (l[1] << 4) | (l[2] << 2) | l[3]


border_lines = "│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌"
border_weights = {weight_index(border_weights_calc(e)): e
                  for e in border_lines}


def border_shader(coord: Vector2, symb: SymbolInfo, context: DrawContext):
    scr = context.screen
    sb = scr.symbol_buffer
    if not (0 <= coord.x < scr.scr_size.x
            and 0 <= coord.y < scr.scr_size.y):
        return
    curr_symb = symb.symbol
    flat_coord = coord.y * scr.scr_size.x + coord.x
    if curr_symb in border_lines:
        symb2 = sb[flat_coord]
        if symb2 in border_lines:
            target_weights = [max(e[0], e[1])
                              for e in zip(border_weights_calc(curr_symb),
                                           border_weights_calc(symb2))]
            try:
                curr_symb = border_weights[weight_index(target_weights)]
            except:
                pass
    if curr_symb != " ":
        sb[flat_coord] = curr_symb
        if not symb.bg_alpha:
            scr.bg_color_buffer[flat_coord] = symb.bg_color
