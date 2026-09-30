"""Builds every 1 Secret FC logo file as outlined SVG (no fonts needed).

The mark: a solid disc (the ball) with a numeral 1 cut out of it. The cut runs
off the bottom edge, so it also reads as the slot of a keyhole."""
import os, sys
from lib import *
from shapely import affinity as A

INK = '#111111'    # Ink
BONE = '#EFEBE3'   # Bone
RED = '#D9442B'    # Signal red (the only accent)
GREY = '#77736C'
NAME = 'InstrumentSans-700'
SUB = 'InstrumentSans-500'


def mark(cx=100, cy=100, r=88):
    """The disc with the 1 cut through it, in a 200 x 200 box by default."""
    s = r / 88
    sw, fw, fd, fs = 24 * s, 24 * s, 22 * s, 18 * s
    x = cx + 6 * s                       # stem sits right of centre so the cut balances
    top = cy - 48 * s
    x0 = x - sw / 2
    one = unary_union([box(x0, top, x + sw / 2, cy + r + 10),
                       Polygon([(x0, top), (x0, top + fd), (x0 - fw, top + fd + fs), (x0 - fw, top + fs)])])
    return Point(cx, cy).buffer(r, 256).difference(one)


def lockup_h(col, sub_col):
    """Mark on the left, name and FUTSAL CLUB on the right. 200 tall."""
    m = mark(100, 100, 88)
    name, w1 = text(NAME, '1 SECRET FC', 58, tracking=14, x=236, y=104, anchor='start')
    sub, w2 = text(SUB, 'FUTSAL CLUB', 22, tracking=10.5, x=238, y=146, anchor='start')
    return [(m, col), (name, col), (sub, sub_col)], 236 + max(w1, w2) + 12


def lockup_v(col, sub_col):
    """Mark above, name below. 360 x 360."""
    m = mark(180, 116, 88)
    name, _ = text(NAME, '1 SECRET FC', 36, tracking=9, x=184, y=276)
    sub, _ = text(SUB, 'FUTSAL CLUB', 15, tracking=7.5, x=184, y=308)
    return [(m, col), (name, col), (sub, sub_col)]


def icon(bg, fg):
    sq = rounded(box(0, 0, 512, 512), 112)
    return [(sq, bg), (mark(256, 256, 170), fg)]


def write(name, w, h, layers, title, bg=None):
    s = svg(w, h, layers, bg=bg, title=title)
    open(os.path.join(OUT_DIR, name), 'w').write(s)
    print(name, len(s) // 1024, 'KB')


if __name__ == '__main__':
    OUT_DIR = sys.argv[1] if len(sys.argv) > 1 else 'out'
    os.makedirs(OUT_DIR, exist_ok=True)
    write('1-secret-fc-mark.svg', 200, 200, [(mark(), INK)], '1 Secret FC mark')
    write('1-secret-fc-mark-white.svg', 200, 200, [(mark(), '#FFFFFF')], '1 Secret FC mark (white)')
    write('1-secret-fc-mark-red.svg', 200, 200, [(mark(), RED)], '1 Secret FC mark (red)')
    L, w = lockup_h(INK, GREY)
    write('1-secret-fc-lockup.svg', round(w), 200, L, '1 Secret FC horizontal lockup')
    L, w = lockup_h(BONE, '#A29D94')
    write('1-secret-fc-lockup-white.svg', round(w), 200, L, '1 Secret FC horizontal lockup (for dark backgrounds)')
    write('1-secret-fc-stacked.svg', 368, 340, lockup_v(INK, GREY), '1 Secret FC stacked lockup')
    write('1-secret-fc-stacked-white.svg', 368, 340, lockup_v(BONE, '#A29D94'), '1 Secret FC stacked lockup (for dark backgrounds)')
    write('1-secret-fc-icon.svg', 512, 512, icon(INK, BONE), '1 Secret FC icon')
    write('1-secret-fc-icon-red.svg', 512, 512, icon(RED, BONE), '1 Secret FC icon (red)')
