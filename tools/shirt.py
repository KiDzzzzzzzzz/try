"""Shirt silhouette used by the kit mockup."""
from lib import *


def jersey_body(back=False):
    neck_dip = 20 if back else 44
    pts = [(146, 26)]
    pts += cubic((146, 26), (166, 26 + neck_dip), (234, 26 + neck_dip), (254, 26))[1:]
    pts += cubic((254, 26), (282, 34), (304, 40), (322, 48))[1:]
    pts += [(394, 128), (344, 176)]
    pts += cubic((344, 176), (330, 164), (324, 156), (318, 146))[1:]
    pts += cubic((318, 146), (316, 240), (320, 340), (322, 422))[1:]
    pts += cubic((322, 422), (250, 432), (150, 432), (78, 422))[1:]
    pts += cubic((78, 422), (80, 340), (84, 240), (82, 146))[1:]
    pts += cubic((82, 146), (76, 156), (70, 164), (56, 176))[1:]
    pts += [(6, 128), (78, 48)]
    pts += cubic((78, 48), (96, 40), (118, 34), (146, 26))[1:]
    return Polygon(pts).buffer(0), neck_dip
