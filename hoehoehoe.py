"""Christmas Ornament"""

import cadquery as cq

msg = "HOEHOEHOE"
thickness = 5
width = 100
overlap_map = {
    "H": 50,
    "O": 52.5,
    "E": 55,
}


result = cq.Workplane("XY")

for c in msg:
    result = result.center(width - overlap_map[c], 0).text(
        c,
        width,
        thickness,
        cut=False,
        combine=True,
        fontPath="./res/courrier_prime_bold.ttf",
        halign="center",
        valign="center",
    )
