"""Shirt mockup, front and back, with the Secret FC emblem."""
import sys
from build import *
from shirt import jersey_body


def jersey_layers(shirt=NAVY, ink=CREAM, back=False):
    body, dip = jersey_body(back)
    neck = cubic((146, 26), (166, 26 + dip), (234, 26 + dip), (254, 26))
    collar = LineString(neck).buffer(3, cap_style=2).intersection(body.buffer(0.5))
    L = [(body, shirt), (collar, ink)]
    g = emblem()
    if not back:
        L.append((A.translate(A.scale(g, 0.19, 0.19, origin=(200, 200)), 62, -84), ink))
    else:
        name, _ = text('SairaCondensed-800', 'SECRET', 30, tracking=10, x=200, y=104)
        L += [(name, ink), (A.translate(A.scale(g, 0.5, 0.5, origin=(200, 200)), -18, 48), ink)]
    return L


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'kit.svg'
    L = jersey_layers() + [(A.translate(g, 440, 0), f) for g, f in jersey_layers(back=True)]
    open(out, 'w').write(svg(840, 440, L, bg='#D9D4CA', title='Secret FC shirt, front and back'))
