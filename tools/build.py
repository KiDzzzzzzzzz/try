"""Builds every 1 Secret FC logo file as outlined SVG (no fonts needed)."""
import os, sys, json
from lib import *
from shapely import affinity as A


INK = '#0B0E14'    # Midnight
BONE = '#F3EFE4'   # Bone
VOLT = '#D4FF3A'   # Volt
GOLD = '#E8B04A'   # Gold (alternate)
MUTE = '#8E8B84'
DISPLAY = 'SairaCondensed-900'
LABEL = 'SairaCondensed-800'


def shield():
    pts = [(62, 22), (338, 22), (372, 56), (372, 258)]
    pts += cubic((372, 258), (372, 372), (292, 428), (200, 464))[1:]
    pts += cubic((200, 464), (108, 428), (28, 372), (28, 258))[1:]
    pts += [(28, 56)]
    return Polygon(pts)


def one_mark(cx=200, top=52, bot=290, sw=100, flag_drop=40, flag_w=50, flag_slope=38,
             kh_cy=138, kh_r=33, slot=(20, 38, 78), ball_r=25.5):
    """The numeral 1 with a keyhole cut through it; the ball sits in the keyhole head."""
    x0, x1 = cx - sw / 2, cx + sw / 2
    stem = box(x0, top, x1, bot)
    flag = Polygon([(x0, top), (x0, top + flag_drop), (x0 - flag_w, top + flag_drop + flag_slope),
                    (x0 - flag_w, top + flag_slope)])
    one = unary_union([stem, flag]).difference(keyhole(cx, kh_cy, kh_r, *slot))
    disc, bink = ball_geom(cx, kh_cy, ball_r, tilt=(0.22, -0.28, 0.1))
    return one, disc, bink


def crest_parts():
    outer = shield()
    ink = inset(outer, 10)
    inner = inset(outer, 20)
    line = inset(outer, 17).difference(inner)
    one, disc, bink = one_mark(cx=210)
    band = box(0, 306, 400, 372).intersection(outer)
    sec, _ = text(DISPLAY, 'SECRET', 62, tracking=7, x=200, y=361)
    fc, _ = text(DISPLAY, 'FC', 38, tracking=5, x=200, y=421)
    side, _ = text(LABEL, 'FUTSAL CLUB', 17, tracking=5)
    side = A.translate(A.rotate(side, 90, origin=(0, 0)), 288, 171)
    return dict(outer=outer, ink=ink, line=line, one=one, disc=disc, bink=bink,
                band=band.difference(sec), fc=fc, side=side)


def crest_layers(acc, side_col=MUTE):
    p = crest_parts()
    return [(p['outer'], acc), (p['ink'], INK), (p['line'], acc), (p['band'], acc),
            (p['one'], acc), (p['disc'], BONE), (p['bink'], INK), (p['fc'], BONE), (p['side'], side_col)]


def crest_mono():
    p = crest_parts()
    return unary_union([p['outer'].difference(p['ink']), p['line'], p['band'], p['one'],
                        p['disc'].difference(p['bink']), p['fc'], p['side']])


def roundel_parts(acc_ring=True):
    cx = cy = 200
    outer = Point(cx, cy).buffer(196, 256)
    ink = Point(cx, cy).buffer(186, 256)
    inner_line = Point(cx, cy).buffer(142, 256).difference(Point(cx, cy).buffer(139, 256))
    top = arc_text(DISPLAY, '1 SECRET FC', 36, cx, cy, 152, center_deg=-90, tracking=6)
    bot = arc_text(LABEL, 'FUTSAL CLUB', 25, cx, cy, 154, center_deg=90, tracking=8, bottom=True)
    dots = unary_union([Point(cx + 164 * s, cy).buffer(5.5, 64) for s in (-1, 1)])
    one, disc, bink = one_mark(cx=212, top=86, bot=314, sw=96, flag_drop=38, flag_w=48,
                               flag_slope=36, kh_cy=170, kh_r=32, slot=(19, 36, 74), ball_r=24.5)
    return dict(outer=outer, ink=ink, line=inner_line, top=top, bot=bot, dots=dots,
                one=one, disc=disc, bink=bink)


def roundel_layers(acc):
    p = roundel_parts()
    return [(p['outer'], acc), (p['ink'], INK), (p['line'], acc), (p['top'], BONE),
            (p['bot'], BONE), (p['dots'], acc), (p['one'], acc), (p['disc'], BONE), (p['bink'], INK)]


def roundel_mono():
    p = roundel_parts()
    return unary_union([p['outer'].difference(p['ink']), p['line'], p['top'], p['bot'], p['dots'],
                        p['one'], p['disc'].difference(p['bink'])])


def icon_layers(acc):
    sq = rounded(box(0, 0, 512, 512), 112)
    # the 1 mark, scaled up and optically centred
    one, disc, bink = one_mark(cx=0, top=0, bot=300, sw=124, flag_drop=50, flag_w=62, flag_slope=46,
                               kh_cy=108, kh_r=41, slot=(25, 47, 96), ball_r=31.5)
    g = unary_union([one, disc])
    minx, miny, maxx, maxy = g.bounds
    dx = 256 - (minx + maxx) / 2 + 12
    dy = 256 - (miny + maxy) / 2
    mv = lambda x: A.translate(x, dx, dy)
    return [(sq, INK), (mv(one), acc), (mv(disc), BONE), (mv(bink), INK)]


def lockup_layers(acc, text_col):
    L = [(A.scale(g, 0.5, 0.5, origin=(0, 0)), f) for g, f in crest_layers(acc)]
    L = [(A.translate(g, 0, 8), f) for g, f in L]
    name, w1 = text(DISPLAY, '1 SECRET FC', 104, tracking=4, x=236, y=146, anchor='start')
    sub, w2 = text(LABEL, 'FUTSAL CLUB', 30, tracking=15.5, x=240, y=196, anchor='start')
    rule = box(240, 160, 240 + w1 - 4, 164)
    light = text_col == INK
    return L + [(name, text_col), (rule, INK if light else acc), (sub, text_col if light else MUTE)], 236 + w1 + 8


def write(name, w, h, layers, title, bg=None):
    s = svg(w, h, layers, bg=bg, title=title)
    open(os.path.join(OUT_DIR, name), 'w').write(s)
    print(name, len(s) // 1024, 'KB')

if __name__ == '__main__':
    OUT_DIR = sys.argv[1] if len(sys.argv) > 1 else 'out'
    os.makedirs(OUT_DIR, exist_ok=True)
    write('1-secret-fc-crest.svg', 400, 480, crest_layers(VOLT), '1 Secret FC crest')
    write('1-secret-fc-crest-gold.svg', 400, 480, crest_layers(GOLD), '1 Secret FC crest (gold)')
    write('1-secret-fc-crest-mono-white.svg', 400, 480, [(crest_mono(), '#FFFFFF')], '1 Secret FC crest (white)')
    write('1-secret-fc-crest-mono-black.svg', 400, 480, [(crest_mono(), INK)], '1 Secret FC crest (black)')
    write('1-secret-fc-roundel.svg', 400, 400, roundel_layers(VOLT), '1 Secret FC roundel')
    write('1-secret-fc-roundel-gold.svg', 400, 400, roundel_layers(GOLD), '1 Secret FC roundel (gold)')
    write('1-secret-fc-roundel-mono-white.svg', 400, 400, [(roundel_mono(), '#FFFFFF')], '1 Secret FC roundel (white)')
    write('1-secret-fc-icon.svg', 512, 512, icon_layers(VOLT), '1 Secret FC icon')
    write('1-secret-fc-icon-gold.svg', 512, 512, icon_layers(GOLD), '1 Secret FC icon (gold)')
    lk, lw = lockup_layers(VOLT, BONE)
    write('1-secret-fc-lockup-dark.svg', round(lw), 256, lk, '1 Secret FC horizontal lockup (for dark backgrounds)')
    lk2, _ = lockup_layers(VOLT, INK)
    write('1-secret-fc-lockup-light.svg', round(lw), 256, lk2, '1 Secret FC horizontal lockup (for light backgrounds)')
