"""Geometry toolkit for the 1 Secret FC logo set: text-to-outline, futsal ball,
keyhole, shields, arched text. Everything is shapely geometry in SVG space
(y down) and is written out as plain filled paths, so the SVGs need no fonts."""
import math
from itertools import product
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from shapely.geometry import Polygon, Point, LineString, MultiPolygon, box
from shapely.ops import unary_union
from shapely import affinity

import os
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts') + os.sep
_font_cache = {}


def font(name):
    if name not in _font_cache:
        _font_cache[name] = TTFont(FONTS + name + '.ttf')
    return _font_cache[name]


# ---------------------------------------------------------------- text
def _flatten(rec, steps=14):
    contours, cur, start = [], [], None
    for op, args in rec.value:
        if op == 'moveTo':
            cur = [args[0]]
        elif op == 'lineTo':
            cur.append(args[0])
        elif op == 'qCurveTo':
            # TrueType implied on-curve points between consecutive off-curves
            pts = list(args)
            p0 = cur[-1]
            offs, end = pts[:-1], pts[-1]
            if end is None:  # closed contour of only off-curve points
                end = ((offs[0][0] + offs[-1][0]) / 2, (offs[0][1] + offs[-1][1]) / 2)
            segs = []
            for i, c in enumerate(offs):
                if i < len(offs) - 1:
                    n = offs[i + 1]
                    e = ((c[0] + n[0]) / 2, (c[1] + n[1]) / 2)
                else:
                    e = end
                segs.append((c, e))
            for c, e in segs:
                for t in range(1, steps + 1):
                    t /= steps
                    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * e[0]
                    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * e[1]
                    cur.append((x, y))
                p0 = e
        elif op == 'curveTo':
            p0 = cur[-1]
            c1, c2, e = args
            for t in range(1, steps + 1):
                t /= steps
                mt = 1 - t
                x = mt**3 * p0[0] + 3 * mt * mt * t * c1[0] + 3 * mt * t * t * c2[0] + t**3 * e[0]
                y = mt**3 * p0[1] + 3 * mt * mt * t * c1[1] + 3 * mt * t * t * c2[1] + t**3 * e[1]
                cur.append((x, y))
        elif op in ('closePath', 'endPath'):
            if len(cur) > 2:
                contours.append(cur)
            cur = []
    return contours


def _signed_area(pts):
    return sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1]
               for i in range(len(pts))) / 2


def glyph(fontname, ch):
    f = font(fontname)
    gs = f.getGlyphSet()
    name = f.getBestCmap()[ord(ch)]
    rec = RecordingPen()
    gs[name].draw(rec)
    outers, holes = [], []
    for c in _flatten(rec):
        p = Polygon(c).buffer(0)
        # TrueType outer contours run clockwise (negative area in y-up space)
        (outers if _signed_area(c) < 0 else holes).append(p)
    g = unary_union(outers).difference(unary_union(holes)) if outers else Polygon()
    return g, gs[name].width, f['head'].unitsPerEm


def text(fontname, s, size, tracking=0.0, x=0.0, y=0.0, anchor='middle'):
    """Outline text; (x, y) is the baseline point at `anchor`. Returns (geom, width)."""
    parts, cx = [], 0.0
    for i, ch in enumerate(s):
        if ch == ' ':
            g, adv, upm = glyph(fontname, ' ')
        else:
            g, adv, upm = glyph(fontname, ch)
        sc = size / upm
        if not g.is_empty:
            g = affinity.scale(g, sc, -sc, origin=(0, 0))
            parts.append(affinity.translate(g, cx, 0))
        cx += adv * sc + (tracking if i < len(s) - 1 else 0)
    width = cx
    geom = unary_union(parts)
    dx = {'start': 0, 'middle': -width / 2, 'end': -width}[anchor]
    return affinity.translate(geom, x + dx, y), width


def cap_height(fontname, size):
    g, _, upm = glyph(fontname, 'H')
    return (g.bounds[3]) * size / upm


def arc_text(fontname, s, size, cx, cy, r, center_deg=-90, tracking=0.0, bottom=False):
    """Text set on a circle. center_deg: angle of the text's middle (SVG degrees,
    -90 = top). Top text reads clockwise with letters' bottoms toward the centre;
    bottom text reads counter-clockwise, upright, with tops toward the centre."""
    items, total = [], 0.0
    for i, ch in enumerate(s):
        g, adv, upm = glyph(fontname, ch)
        sc = size / upm
        w = adv * sc
        items.append((g, sc, w))
        total += w + (tracking if i < len(s) - 1 else 0)
    ch_h = cap_height(fontname, size)
    rr = r if not bottom else r + ch_h  # baseline radius
    arc_len_total = total / rr
    parts, pos = [], 0.0
    for g, sc, w in items:
        mid = pos + w / 2
        if not bottom:
            ang = math.radians(center_deg) - arc_len_total / 2 + mid / rr
        else:
            ang = math.radians(center_deg) + arc_len_total / 2 - mid / rr
        if not g.is_empty:
            gg = affinity.scale(g, sc, -sc, origin=(0, 0))
            gg = affinity.translate(gg, -w / 2, 0)  # centre glyph on its advance
            if not bottom:
                gg = affinity.translate(gg, 0, -r)          # baseline at radius r above centre
                gg = affinity.rotate(gg, math.degrees(ang) + 90, origin=(0, 0))
            else:
                gg = affinity.translate(gg, 0, rr)          # baseline below centre
                gg = affinity.rotate(gg, math.degrees(ang) - 90, origin=(0, 0))
            parts.append(affinity.translate(gg, cx, cy))
        pos += w + tracking
    return unary_union(parts)


# ---------------------------------------------------------------- ball
PHI = (1 + 5 ** 0.5) / 2


def _cyc(v):
    a, b, c = v
    return [(a, b, c), (b, c, a), (c, a, b)]


def _signs(v):
    out = set()
    for s in product([1, -1], repeat=3):
        out.add(tuple(x * sx for x, sx in zip(v, s)))
    return out


def _norm(v):
    l = math.sqrt(sum(x * x for x in v))
    return tuple(x / l for x in v)


def _rot(v, ax, ang):
    x, y, z = v
    c, s = math.cos(ang), math.sin(ang)
    if ax == 'x':
        return (x, c * y - s * z, s * y + c * z)
    if ax == 'y':
        return (c * x + s * z, y, -s * x + c * z)
    return (c * x - s * y, s * x + c * y, z)


def _ti():
    verts = set()
    for base in [(0, 1, 3 * PHI), (1, 2 + PHI, 2 * PHI), (PHI, 2, 2 * PHI + 1)]:
        for sv in _signs(base):
            for p in _cyc(sv):
                verts.add(tuple(round(x, 9) for x in p))
    verts = list(verts)
    assert len(verts) == 60, len(verts)
    pent_n = set()
    for sv in _signs((0, 1, PHI)):
        for p in _cyc(sv):
            pent_n.add(p)
    hex_n = set(_signs((1, 1, 1)))
    for sv in _signs((0, PHI, 1 / PHI)):
        for p in _cyc(sv):
            hex_n.add(p)
    faces = []
    for normals, k, kind in [(pent_n, 5, 'p'), (hex_n, 6, 'h')]:
        for n in normals:
            n = _norm(n)
            ds = sorted(verts, key=lambda v: -sum(a * b for a, b in zip(v, n)))[:k]
            faces.append((kind, n, ds))
    return faces


def ball_geom(cx, cy, r, seam=None, tilt=(0.0, 0.0, 0.0), theta_max=78):
    """32-panel ball drawn with an azimuthal-equidistant projection (the look of
    a classic ball icon: panels stay readable all the way to the rim).
    Returns (disc, ink): the white ball and its pentagons plus seams."""
    seam = seam if seam is not None else r * 0.05
    tmax = math.radians(theta_max)
    faces = _ti()
    n0 = _norm((0, 1, PHI))
    a1 = math.atan2(n0[1], n0[2])

    def orient(v):
        v = _rot(v, 'x', a1)
        v = _rot(v, 'z', math.radians(18))
        v = _rot(v, 'x', tilt[0])
        v = _rot(v, 'y', tilt[1])
        v = _rot(v, 'z', tilt[2])
        return v

    def proj(p):
        th = math.acos(max(-1, min(1, p[2])))
        az = math.atan2(p[1], p[0])
        rho = th / tmax * r
        return (cx + rho * math.cos(az), cy - rho * math.sin(az)), th

    disc = Point(cx, cy).buffer(r, 180)
    pents, seams = [], []
    for kind, n, vs in faces:
        n2 = orient(n)
        vs2 = [orient(v) for v in vs]
        c = tuple(sum(v[i] for v in vs2) / len(vs2) for i in range(3))
        u = _norm(tuple(vs2[0][i] - c[i] for i in range(3)))
        w = (n2[1] * u[2] - n2[2] * u[1], n2[2] * u[0] - n2[0] * u[2], n2[0] * u[1] - n2[1] * u[0])
        vs2.sort(key=lambda v: math.atan2(sum((v[i] - c[i]) * w[i] for i in range(3)),
                                          sum((v[i] - c[i]) * u[i] for i in range(3))))
        ring, ths = [], []
        for i in range(len(vs2)):
            a, b = vs2[i], vs2[(i + 1) % len(vs2)]
            for t in range(16):
                t /= 16
                p = _norm(tuple(a[j] + (b[j] - a[j]) * t for j in range(3)))
                xy, th = proj(p)
                ring.append(xy)
                ths.append(th)
        if min(ths) > tmax:
            continue
        if kind == 'p':
            pents.append(Polygon(ring).buffer(0))
        seams.append(LineString(ring + [ring[0]]))
    ink = unary_union(pents + [unary_union(seams).buffer(seam / 2, cap_style=1, join_style=1)])
    return disc, ink.intersection(disc)


# ---------------------------------------------------------------- shapes
def keyhole(cx, cy, r, top_w, bot_w, length, radius_bottom=0):
    """Keyhole: circle of radius r centred at (cx, cy) plus a tapered slot."""
    head = Point(cx, cy).buffer(r, 128)
    y0 = cy
    slot = Polygon([(cx - top_w / 2, y0), (cx + top_w / 2, y0),
                    (cx + bot_w / 2, cy + r + length), (cx - bot_w / 2, cy + r + length)])
    return unary_union([head, slot])


def rounded(geom, rad):
    return geom.buffer(-rad, join_style=1).buffer(rad, join_style=1) if rad else geom


def cubic(p0, c1, c2, p1, n=40):
    return [((1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * c1[0] + 3 * (1 - t) * t * t * c2[0] + t ** 3 * p1[0],
             (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * c1[1] + 3 * (1 - t) * t * t * c2[1] + t ** 3 * p1[1])
            for t in [i / n for i in range(n + 1)]]


def inset(geom, d):
    return geom.buffer(-d, join_style=2, mitre_limit=4)


def outset(geom, d, round_join=False):
    return geom.buffer(d, join_style=1 if round_join else 2, mitre_limit=4)


# ---------------------------------------------------------------- output
def path_d(geom, nd=2):
    if geom.is_empty:
        return ''
    polys = [geom] if isinstance(geom, Polygon) else [g for g in getattr(geom, 'geoms', []) if isinstance(g, Polygon)]
    if not polys and hasattr(geom, 'geoms'):
        polys = []
        for g in geom.geoms:
            if isinstance(g, Polygon):
                polys.append(g)
            elif isinstance(g, MultiPolygon):
                polys.extend(g.geoms)
    fmt = lambda v: ('%.*f' % (nd, v)).rstrip('0').rstrip('.')
    out = []
    from shapely.geometry.polygon import orient
    for p in polys:
        p = orient(p.simplify(0.04), 1.0)  # outer rings one way, holes the other: fills right under nonzero too
        for ring in [p.exterior] + list(p.interiors):
            cs = list(ring.coords)[:-1]
            if len(cs) < 3:
                continue
            out.append('M' + fmt(cs[0][0]) + ' ' + fmt(cs[0][1]) +
                       ''.join('L' + fmt(x) + ' ' + fmt(y) for x, y in cs[1:]) + 'Z')
    return ''.join(out)


def svg(w, h, layers, bg=None, title=None):
    body = []
    if title:
        body.append('<title>%s</title>' % title)
    if bg:
        body.append('<rect width="%g" height="%g" fill="%s"/>' % (w, h, bg))
    for geom, fill in layers:
        d = path_d(geom)
        if d:
            body.append('<path fill="%s" fill-rule="evenodd" d="%s"/>' % (fill, d))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %g %g">' % (w, h)
            + ''.join(body) + '</svg>')
