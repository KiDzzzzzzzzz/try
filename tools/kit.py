from build import *

def jersey_body(back=False):
    """Short-sleeve futsal shirt, 400 x 440."""
    neck_dip = 20 if back else 44
    pts = [(146, 26)]
    pts += cubic((146, 26), (166, 26 + neck_dip), (234, 26 + neck_dip), (254, 26))[1:]
    pts += cubic((254, 26), (282, 34), (304, 40), (322, 48))[1:]           # right shoulder
    pts += [(394, 128), (344, 176)]                                          # right sleeve
    pts += cubic((344, 176), (330, 164), (324, 156), (318, 146))[1:]
    pts += cubic((318, 146), (316, 240), (320, 340), (322, 422))[1:]         # right side
    pts += cubic((322, 422), (250, 432), (150, 432), (78, 422))[1:]          # hem
    pts += cubic((78, 422), (80, 340), (84, 240), (82, 146))[1:]             # left side
    pts += cubic((82, 146), (76, 156), (70, 164), (56, 176))[1:]
    pts += [(6, 128), (78, 48)]                                               # left sleeve
    pts += cubic((78, 48), (96, 40), (118, 34), (146, 26))[1:]
    return Polygon(pts).buffer(0), neck_dip

def jersey_layers(acc, back=False):
    body, dip = jersey_body(back)
    # collar: a band following the neckline
    neck = cubic((146, 26), (166, 26 + dip), (234, 26 + dip), (254, 26))
    collar = LineString(neck).buffer(7, cap_style=2).intersection(body.buffer(0.5))
    # sleeve cuffs: stripes parallel to the sleeve ends
    cuffR = Polygon([(394, 128), (344, 176), (334, 166), (384, 118)]).intersection(body)
    cuffL = Polygon([(6, 128), (56, 176), (66, 166), (16, 118)]).intersection(body)
    L = [(body, INK), (collar, acc), (cuffR, acc), (cuffL, acc)]
    if not back:
        cr = [(A.translate(A.scale(g, 0.15, 0.15, origin=(0, 0)), 234, 92), f) for g, f in crest_layers(acc)]
        L += cr
    else:
        name, _ = text(DISPLAY, 'SECRET', 40, tracking=6, x=200, y=112)
        one, disc, bink = one_mark(cx=0, top=0, bot=190, sw=78, flag_drop=32, flag_w=40, flag_slope=30,
                                   kh_cy=70, kh_r=26, slot=(16, 30, 60), ball_r=20)
        g = unary_union([one, disc]); minx, miny, maxx, maxy = g.bounds
        mv = lambda x: A.translate(x, 200 - (minx + maxx) / 2 + 8, 136 - miny)
        L += [(name, BONE), (mv(one), acc), (mv(disc), BONE), (mv(bink), INK)]
    return L

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'home-kit.svg'
    L = jersey_layers(VOLT) + [(A.translate(g, 440, 0), f) for g, f in jersey_layers(VOLT, back=True)]
    open(out, 'w').write(svg(840, 440, L, bg='#F3EFE4', title='1 Secret FC home kit, front and back'))
