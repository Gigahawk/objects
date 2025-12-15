"""LCD cover mounting arms for a Prusa MK3

Line for line translation of
https://github.com/prusa3d/Original-Prusa-i3/blob/MK3S/Printed-Parts/SCAD/lcd-supports.scad
"""

from build123d import *


def cube(lwh):
    """Approximation of OpenSCAD cube()"""
    return Box(lwh[0], lwh[1], lwh[2], align=Align.MIN)


def cylinder(h, r1, r2=None):
    align = (Align.CENTER, Align.CENTER, Align.MIN)
    if r2 is not None:
        return Cone(height=h, bottom_radius=r1, top_radius=r2, align=align)
    return Cylinder(height=h, radius=r1, align=align)


class RegularPrism(BasePartObject):
    """Approximation of OpenSCAD cyl()"""

    def __init__(self, h, r, fn):
        with BuildPart() as part:
            with BuildSketch():
                RegularPolygon(r, fn)
            extrude(amount=h)
        super().__init__(part.part)


# Main body
# base block
body = Location((-55, -2, 0)) * cube([69, 81, 10])
# outer body shape
body -= Location((-69.6, 32, -1), (0, 0, 45)) * cube([60, 53, 15])
body -= Location((13.7, 89.7, -1), (0, 0, 135)) * cube([60, 42, 15])
body -= Location((-19, -9, -1)) * cube([60, 9, 15])
body -= Location((7, -3, -1)) * cube([60, 68, 16])
body -= Location((-16, 60, -1)) * cube([60, 50, 15])
body -= Location((-41, -45, -1), (0, 0, 45)) * cube([60, 80, 13])
# pcb cout out
body -= Location((4, 1.5, -1)) * cube([1.8, 56.5, 17])
body -= Location((0, 7.5, -1)) * cube([5.8, 44.5, 17])
body -= Location((4.8, 3.5, -1)) * cube([5.8, 52.5, 17])
body -= Location((8, -5, -1), (0, 0, 45)) * cube([5, 5, 17])
body -= Location((8, 58, -1), (0, 0, 45)) * cube([5, 5, 17])
# pcb inserts
body -= Location((4, 3, 8), (45, 0, 0)) * cube([1.8, 5, 5])
body -= Location((4, 56.5, 8), (45, 0, 0)) * cube([1.8, 5, 5])
body -= Location((4, 3, -5), (45, 0, 0)) * cube([1.8, 5, 5])
body -= Location((4, 56.5, -5), (45, 0, 0)) * cube([1.8, 5, 5])

# Base support piece
support = Location((0, 0, 0), (0, 0, 45)) * body
support += Location((-72, 22, 0)) * cube([30, 16, 10])
# lower angled part cut
support -= Location((-75, -2, -1)) * cube([20, 14, 15])
support -= Location((-70, -2, -1)) * cube([20, 14, 15])
support -= Location((-50, -16.3, -1), (0, 0, 45)) * cube([20, 20, 15])

support -= Location((-76.5, -2, -1)) * cube([15, 40, 15])

support -= (
    Location((-28, 0, -1), (0, 0, 45)) * cube([10, 40, 15])
    - Location((-38, -12, -1)) * cube([20, 20, 15])
    - Location((-58, 23.5, -1)) * cube([25, 25, 15])
)
# screw holes
support -= Location((-71, 18 + 4, 5), (0, 90, 0)) * cylinder(h=22, r1=1.75)
support -= Location((-70, 29 + 4, 5), (0, 90, 0)) * cylinder(h=22, r1=1.75)
# nut traps
support -= Location((-58, 15.1 + 4, 5 - 2.8)) * cube([2.2, 5.8, 29.7])
support -= Location((-58, 26.1 + 4, 5 - 2.8)) * cube([2.2, 5.8, 29.7])
# version
# OpenSCAD font size works different from OCC
text_scale_constant = 1.35
support -= Location((-20, 2, 9.5)) * extrude(
    Text(
        "R1",
        font_size=5 * text_scale_constant,
        font_style=FontStyle.BOLD,
        font="Liberation Sans",
        # (openscad's center=true doesn't seem to do anything for text,
        # the locations specified in the original code are for minimum alignment)
        align=Align.MIN,
    ),
    amount=0.6,
)

right_support = support
left_support = support
left_support += Location((0, 0, 0), (0, 0, 45)) * (
    # sd card shield
    Location((-3, 3, 10)) * cube([2, 55, 10])
    - Location((-4, 3, 20), (0, 90, 0)) * cylinder(h=4, r1=7)
    - Location((-4, 58, 20), (0, 90, 0)) * cylinder(h=4, r1=7)
)


results = {"left": left_support, "right": right_support}


try:
    from ocp_vscode import *

    show_all()
except:
    pass
