"""Secret FC emblem: a ball with a keyhole at its centre, swooshes wrapping round it,
a keyhole breaking out of the ring, and the name set on the ring."""
import math, os, sys
from lib import *
from shapely import affinity as A
CREAM='#EDE6D6'; NAVY='#101A2C'
C=(200,200)
def ring(cx,cy,r,w): return Point(cx,cy).buffer(r+w/2,256).difference(Point(cx,cy).buffer(r-w/2,256))
def span(a0,a1,c=C):
    return Polygon([c]+[(c[0]+500*math.cos(math.radians(a0+i*(a1-a0)/60)),c[1]+500*math.sin(math.radians(a0+i*(a1-a0)/60))) for i in range(61)])
def kh_shape(s=1.0):
    return unary_union([Point(0,-5*s).buffer(6*s,64), Polygon([(-2.8*s,-5*s),(2.8*s,-5*s),(5.4*s,12*s),(-5.4*s,12*s)])])
def swoosh(c,a0,a1,r0,r1,wmax,peak=0.35,p=1.3,n=160):
    L,R=[],[]
    for i in range(n+1):
        t=i/n; a=math.radians(a0+(a1-a0)*t); r=r0+(r1-r0)*t**p
        x,y=c[0]+r*math.cos(a),c[1]+r*math.sin(a)
        # tangent
        t2=min(1,t+1e-3); a2=math.radians(a0+(a1-a0)*t2); r2=r0+(r1-r0)*t2**p
        tx,ty=c[0]+r2*math.cos(a2)-x, c[1]+r2*math.sin(a2)-y; l=math.hypot(tx,ty) or 1
        nx,ny=-ty/l,tx/l
        u=t/peak if t<peak else (1-t)/(1-peak)
        w=wmax*math.sin(u*math.pi/2)**0.9/2
        L.append((x+nx*w,y+ny*w)); R.append((x-nx*w,y-ny*w))
    return Polygon(L+R[::-1]).buffer(0)
def ball_panels(bc,br):
    """the ball's pentagon panels, no seams; the front panel carries a keyhole"""
    import lib
    faces=lib._ti(); n0=lib._norm((0,1,PHI)); a1=math.atan2(n0[1],n0[2])
    tilt=(0.12,-0.22,0.2); tmax=math.radians(80)
    def orient(v):
        v=lib._rot(v,'x',a1); v=lib._rot(v,'z',math.radians(18))
        for ax,tt in zip('xyz',tilt): v=lib._rot(v,ax,tt)
        return v
    def proj(p):
        th=math.acos(max(-1,min(1,p[2]))); az=math.atan2(p[1],p[0]); rho=th/tmax*br
        return (bc[0]+rho*math.cos(az), bc[1]-rho*math.sin(az)), th
    out=[]; front=None
    for kind,n,vs in faces:
        if kind!='p': continue
        nv=orient(n)
        vs2=[orient(v) for v in vs]
        pts=[proj(lib._norm(v)) for v in vs2]
        if min(t for _,t in pts)>tmax: continue
        poly=Polygon([p for p,_ in pts]).convex_hull
        poly=A.scale(poly,0.86,0.86,origin=poly.centroid)
        if nv[2]>0.9: front=poly
        out.append(poly)
    g=unary_union(out)
    if front is not None:
        c=front.centroid; k=A.translate(kh_shape(2.9),c.x,c.y+2)
        g=g.difference(front.buffer(0.5)).union(k)
    return g.intersection(Point(*bc).buffer(br-9,256))
def emblem():
    bc=(214,206); br=84
    ballr=ring(*bc,br,7)
    panels=ball_panels(bc,br)
    s1=swoosh(bc,122,318,114,178,22,peak=0.38)
    s2=swoosh(bc,148,250,99,116,11,peak=0.5)
    s3=swoosh(bc,-25,78,97,112,12,peak=0.6)
    # breakout keyhole outline at the end of the big swoosh
    kpos=(bc[0]+188*math.cos(math.radians(-44)), bc[1]+188*math.sin(math.radians(-44)))
    k=A.rotate(kh_shape(2.8),46,origin=(0,0)); k=A.translate(k,*kpos)
    kout=k.buffer(7).difference(k)
    sw=unary_union([s1,s2,s3,kout])
    name=arc_text('SairaCondensed-800','SECRET FC',42,*C,150,center_deg=12,tracking=5)
    lab=arc_text('SairaCondensed-800','FUTSAL CLUB',18,*C,153,center_deg=96,tracking=4,bottom=True)
    outer=ring(*C,160,6).difference(span(-40,66)).difference(span(65,121))
    dots=unary_union([Point(C[0]+160*math.cos(math.radians(a)),C[1]+160*math.sin(math.radians(a))).buffer(5,64) for a in (-36,62)])
    gap=sw.buffer(6)
    under=unary_union([outer,ballr,panels,dots]).difference(gap)
    return unary_union([under,sw,name,lab])

NAVY_T = '#0E1728'


def fabric(w, h, bg=NAVY):
    """Woven-fabric backdrop for mockups (a fine grid of soft dots)."""
    return ('<defs><pattern id="weave" width="6" height="6" patternUnits="userSpaceOnUse">'
            '<rect width="6" height="6" fill="%s"/><rect x="0.6" y="0.6" width="4.2" height="4.2" rx="1.6" fill="#16223A"/>'
            '</pattern><radialGradient id="shade" cx="40%%" cy="35%%" r="80%%">'
            '<stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.45"/>'
            '</radialGradient></defs><rect width="%g" height="%g" fill="url(#weave)"/>'
            '<rect width="%g" height="%g" fill="url(#shade)"/>' % (bg, w, h, w, h))


def write(name, w, h, layers, title, bg=None, extra=''):
    s = svg(w, h, layers, bg=bg, title=title)
    if extra:
        s = s.replace('</title>', '</title>' + extra, 1)
    open(os.path.join(OUT_DIR, name), 'w').write(s)
    print(name, len(s) // 1024, 'KB')


if __name__ == '__main__':
    OUT_DIR = sys.argv[1] if len(sys.argv) > 1 else 'out'
    os.makedirs(OUT_DIR, exist_ok=True)
    g = emblem()
    write('secret-fc-emblem-cream.svg', 400, 400, [(g, CREAM)], 'Secret FC emblem (cream, for dark backgrounds)')
    write('secret-fc-emblem-navy.svg', 400, 400, [(g, NAVY)], 'Secret FC emblem (navy, for light backgrounds)')
    write('secret-fc-emblem-on-navy.svg', 400, 400, [(g, CREAM)], 'Secret FC emblem on navy', bg=NAVY)
    big = A.translate(A.scale(g, 1.6, 1.6, origin=(200, 200)), 200, 200)
    write('secret-fc-fabric-mockup.svg', 800, 800, [(big, CREAM)], 'Secret FC emblem on navy fabric', extra=fabric(800, 800))
