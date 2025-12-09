"""Z axis top for a Prusa MK3

Line for line translation of 
https://github.com/prusa3d/Original-Prusa-i3/blob/MK3S/Printed-Parts/SCAD/z-axis-top.scad
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


z_top_base = Location((0, -5, 0)) * cube([8, 45, 16])  # plate touching the base
z_top_base += Location((0, -5, 0)) * cube([33, 3.6, 12])  # plate touching the base
z_top_base += Location((0, -5, 0)) * cube([38, 45, 5])  # plate touching the base
z_top_base += Location((25 + 4.3, 3.2, 5), (0, 0, 0)) * cylinder(h=2.5, r1=7)

# Corner cutouts
z_top_fancy = Location((0.5, 0.5, 0), (0, 0, -45 - 180)) * Location((-15, 0, -1)) * cube([30, 30, 51])

# frame side angle
z_top_fancy += Location((-13, 40 + 5 + 10.2, -3), (0, 0, -45 - 0)) * Location((0, 0, -1)) * cube([30, 30, 51])
z_top_fancy += Location((8, 28, -3)) * Location((0, 0, -1)) * cube([50, 50, 51])

# cut to shape
z_top_fancy += Location((4, -1, 12), (0, 0, 0)) * Location((0, -5, 0)) * cube([30, 50, 30])
z_top_fancy += Location((6, 0, 12), (0, -45, 0)) * Location((0, -5, 0)) * cube([30, 50, 30])
z_top_fancy += Location((8, 3.9, 10), (0, -45, 0)) * Location((0, -5, 0)) * cube([30, 50, 30])

# nice edges
z_top_fancy += Location((38 - 2.5, -5 + 2.5, -3), (0, 0, -45 - 90)) * Location((-15, 0, -1)) * cube([30, 30, 51])
z_top_fancy += Location((-10, 49, 3.2), (45, 0, 0)) * Location((0, 0, 0), (0, 0, -45 + 90)) * Location((0, 0, -15)) * cube([30, 30, 30])

# outer corner
z_top_fancy += Location((35, 26, -3), (0, 0, -45)) * Location((-15, 0, -1)) * cube([30, 30, 51])
z_top_fancy += Location((0, 0, 5), (45 + 180, 0, 0)) * Location((0, 0, 0), (0, 0, -45 + 90)) * Location((0, 0, -15)) * cube([30, 30, 30])

# Stiffner cut out
z_top_fancy += Location((33, -1, 7.5), (0, -45, 0)) * Location((0, -5, 0)) * cube([30, 50, 30])

# side cut out
z_top_fancy += Location((-6, -5, -5.55), (45, 0, 0)) * cube([50, 5, 5])
z_top_fancy += Location((-6, -5, -0.8), (0, 45, 0)) * cube([5, 50, 5])

# Screw holes frame
z_top_holes = Location((-1, 10, 10), (0, 90, 0)) * cylinder(h=20, r1=1.6)
z_top_holes += Location((-1, 10 + 20, 10), (0, 90, 0)) * cylinder(h=20, r1=1.6)

# Screw heads
z_top_holes += Location((4, 10, 10), (0, 90, 0)) * cylinder(h=20, r1=3.1)
z_top_holes += Location((4, 10 - 3.1, 10)) * cube([10, 6.2, 10])
z_top_holes += Location((4, 10 + 20, 10), (0, 90, 0)) * cylinder(h=20, r1=3.1)
z_top_holes += Location((4, 10 + 20 - 3.1, 10)) * cube([10, 6.2, 10])

# Z rod holder
z_top_holes += Location((25 + 4.3, 3, 0.6), (0, 0, 0)) * cylinder(h=50, r1=4.05)
z_top_holes += Location((25 + 4.3, 3, 3.4), (0, 0, 0)) * cylinder(h=4.2, r2=4.3, r1=4.05)

# material saving cut
z_top_holes += Location((16, 10, -4), (0, 0, 0)) * RegularPrism(h=50, r=8, fn=6)
z_top_holes += Location((16, 28, -4), (0, 0, 0)) * RegularPrism(h=50, r=8, fn=6)

# z screw hole
z_top_holes += Location((25 + 4.3, 3 + 17, 3), (0, 0, 0)) * cylinder(h=50, r1=5.8)  # screw hole
z_top_holes += Location((25 + 4.3, 3 + 17, 0.6), (0, 0, 0)) * cylinder(h=50, r1=5.8)  # screw hole
z_top_holes += Location((25 + 4.3 - 1, 3, 0.6)) * cube([2, 15, 8])  # it's bit up because it helps with printing

# selective infill
z_top_holes += Location((36.5, 1.5, 0.5)) * cube([0.1, 20, 3.5])
z_top_holes += Location((10, -3, 0.5)) * cube([22, 0.1, 3.5])
z_top_holes += Location((3, 1, 0.5)) * cube([18, 0.1, 3.5])
z_top_holes += Location((1.5, 19, 0.5)) * cube([21, 0.1, 3.5])

z_top_right = z_top_base
z_top_right -= z_top_fancy
z_top_right -= z_top_holes

z_top_left = z_top_right.mirror(Plane.XZ)

# Version right
version_txt = "R2"
# OpenSCAD font size works different from OCC
text_scale_constant = 1.35
z_top_right -= (
    # build123d's rotation order is different from OpenSCADs
    Location((12, -1.5, 10), (0, 0, 180)) * Location((0, 0, 0), (0, 180, 0)) * Location((0, 0, 0), (90, 0, 0))
    * extrude(
        Text(
            version_txt, font_size=4*text_scale_constant, font_style=FontStyle.BOLD, font="Liberation Sans", 
            align=Align.MIN), 
        amount=0.6
    )
)

# Version left
z_top_left -= (
    # build123d's rotation order is different from OpenSCADs
    # Location is wrong, original source is (19, -1, 10), but has to be like this due to the differences
    # in how mirror works in openscad and b3d
    Location((19, 1.5, 10), (0, 180, 0)) * Location((0, 0, 0), (90, 0, 0))
    * extrude(
        Text(
            version_txt, font_size=4*text_scale_constant, font_style=FontStyle.BOLD, font="Liberation Sans", 
            align=Align.MIN), 
        amount=0.6
    )
)

z_top_left = Location((0, -12, 0)) * z_top_left

results = {
    "left": z_top_left,
    "right": z_top_right,
}

if "show_object" in locals():
    show_object(z_top_base)

try:
    from ocp_vscode import *
    show(z_top_right, z_top_left)
except:
    pass