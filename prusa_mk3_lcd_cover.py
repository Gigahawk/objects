"""LCD cover for a Prusa MK3

Line for line translation of
https://github.com/prusa3d/Original-Prusa-i3/blob/MK3S/Printed-Parts/SCAD/LCD-cover-ORIGINAL-MK3.scad
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
main_body = Location((-77, -4.5, 0)) * cube([155, 59.8, 2])
main_body += Location((-77, -4.5, 0), (35, 0, 0)) * cube([155, 3, 20.08])
# HACK: add extra padding to fix weird geometry issue on front corner
main_body += Location((-77, -4.6, -0.1), (35, 0, 0)) * cube([155, 3, 20.08])
main_body += Location((-77, -3.5, -1), (35, 0, 0)) * cube([7, 5, 15])
main_body += Location((71, -3.5, -1), (35, 0, 0)) * cube([7, 5, 15])
main_body += Location((-77, -15.2, 14.2)) * cube([155, 3.1, 11.8])
main_body += Location((-77, 54, 0)) * cube([155, 2, 17])
# M3 hole body
main_body += Location((73.5, 43.3, 0.5), (0, 0, 90)) * RegularPrism(h=14, r=4, fn=6)
main_body += Location((-72.5, 43.3, 0.5), (0, 0, 90)) * RegularPrism(h=14, r=4, fn=6)

lcd_window = Location((-61.5, 1, 1.2)) * cube([98.5, 42, 10])
lcd_window += Location((-52.5, 8, -1)) * cube([80, 30.5, 10])
main_body -= lcd_window

speaker_grill = Part()
for buzz in range(55, 68, 2):
    speaker_grill += Location((buzz, 1.5, -1)) * cube([1.3, 4, 10])
    speaker_grill += Location((buzz - 0.75, 1.5, -0.5), (0, 45, 0)) * cube([2, 4, 2])
    if buzz < 67:
        speaker_grill += Location((buzz + 1.25, 1.5, -0.5), (0, 45, 0)) * cube(
            [2, 4, 2]
        )
main_body -= speaker_grill

knob_hole = Location((62.5, 21, -1)) * cylinder(h=10, r1=6)
knob_hole += Location((62.5, 21, -1.2)) * cylinder(h=2, r1=7, r2=6)
main_body -= knob_hole

# vertical lines
reset_button_cutout = Location((44, 26, -1)) * cube([1, 6, 9])
reset_button_cutout += Location((48, 26, -1)) * cube([1, 2.5, 9])
reset_button_cutout += Location((68.5, 36, -1)) * cube([1, 8, 9])
# horizontal lines
reset_button_cutout += Location((56, 43, -1)) * cube([13.5, 1, 9])
reset_button_cutout += Location((50.5, 30, -1)) * cube([13, 1, 9])
# angled lines
reset_button_cutout += Location((44.7, 31.28, -1), (0, 0, 45)) * cube([17, 1, 9])
reset_button_cutout += Location((63.5, 30, -1), (0, 0, 45)) * cube([8.5, 1, 9])
reset_button_cutout += Location((48.7, 27.8, -1), (0, 0, 45)) * cube([3.55, 1, 9])
main_body -= reset_button_cutout

rear_support_cutout = Location((-64.5, -12.1, 14)) * cube([10, 3, 16])
rear_support_cutout += Location((55.5, -12.1, 14)) * cube([10, 3, 16])
main_body -= rear_support_cutout

# Bottom flange?
bottom_flange = Location((-70, 55.5, -2), (55, 0, 0)) * cube([120, 5, 5])
bottom_flange -= Location((-100, 40, -9.5)) * cube([200, 50, 10])
main_body += bottom_flange

pcb_clip = Location((-3, -12, 17.5)) * cube([7, 4, 5])
pcb_clip += Location((-3, -10.6, 12.5)) * cube([1, 2.6, 7])
pcb_clip += Location((3, -10.6, 12.5)) * cube([1, 2.6, 7])
pcb_clip -= Location((-4, -8, 18.5), (30, 0, 0)) * cube([10, 6, 6])
pcb_clip -= Location((2.5, -12, 14.5)) * cube([1, 4, 0.2])
pcb_clip -= Location((-2.5, -12, 14.5)) * cube([1, 4, 0.2])
pcb_clip -= Location((2.5, -12, 17.3)) * cube([1, 4, 0.2])
pcb_clip -= Location((-2.5, -12, 17.3)) * cube([1, 4, 0.2])


base_result = pcb_clip + main_body

# Reset button extension
base_result += Location((62.5, 37.3, 0)) * cylinder(h=7.2, r1=3.5)

# Left side
base_result += Location((-77, -14.7, 0)) * cube([1.5, 70.7, 26])
base_result += Location((-76.5, -15, 0)) * cube([4, 70, 14.5])

# Right side
base_result += Location((76.5, -14.7, 0)) * cube([1.5, 70.7, 26])
base_result += Location((73.6, -14, 0)) * cube([4, 70, 14.5])

# Rear side reinforcement
base_result += Location((-54.5, -11.7, 8)) * cube([110, 4, 6.5])
base_result += Location((65.5, -11.7, 8)) * cube([12, 4, 6.5])
base_result += Location((65.5, -13, 14)) * cube([12, 2, 12])
base_result += Location((-76.5, -11.7, 8)) * cube([12, 4, 6.5])
base_result += Location((-76.5, -14.7, 14.5)) * cube([12, 4, 11.5])
base_result += Location((-44, -14.7, 14.5)) * cube([89, 4, 11.5])
base_result += Location((-43.5, -10.7, 15), (90, 0, 0)) * cylinder(h=2, r1=11)
base_result += Location((44.5, -10.7, 15), (90, 0, 0)) * cylinder(h=2, r1=11)

# Front left side reinforcement
front_left_side_reinforcement = Location((-77, 41.3, 0)) * cube([15, 14, 25])
front_left_side_reinforcement += Location((-77, 46.3, 14)) * cube([15, 9, 3])
front_left_side_reinforcement -= Location((-64.5, 40, -3)) * cube([4, 8, 40])
front_left_side_reinforcement -= Location((-75.5, 40.3, 14.5)) * cube([15, 6.5, 25])
base_result += front_left_side_reinforcement

# Front right side reinforcement
front_right_side_reinforcement = Location((38, 41.2, 0)) * cube([40, 14, 26])
front_right_side_reinforcement -= Location((55, 44.5, 0)) * cube([10.5, 3.7, 30])
front_right_side_reinforcement -= Location((44, 39.5, 0)) * cube([25.5, 5, 30])
front_right_side_reinforcement -= Location((35, 39.3, 14.5)) * cube([42.5, 7, 15])
front_right_side_reinforcement -= Location((49, 43.2, 25), (0, 60, 0)) * cube(
    [12, 5, 10]
)
base_result += front_right_side_reinforcement

# SD card opening
base_result -= Location((-80, 9, 16.5)) * cube([10, 28, 4.5])

# Front and rear angle
base_result -= Location((-81, -10.5, -17), (32, 0, 0)) * cube([164, 14, 54.08])
base_result -= Location((-78, 72.7, -3), (45, 0, 0)) * cube([160, 14, 54.08])

# M3 screw thread
base_result -= Location((72.5, 42.7, 3)) * cylinder(h=20, r1=1.4)
base_result -= Location((-72.5, 42.7, 3)) * cylinder(h=20, r1=1.4)
base_result -= Location((72.5, 42.7, 11.7)) * cylinder(h=3, r1=1.4, r2=2.2)
base_result -= Location((-72.5, 42.7, 11.7)) * cylinder(h=3, r1=1.4, r2=2.2)


# ORIGINAL PRUSA text
# OpenSCAD font size works different from OCC
text_scale_constant = 1.35
base_result -= Location((-67, 51, 0.6), (180, 0, 0)) * extrude(
    Text(
        "ORIGINAL",
        font_size=7 * text_scale_constant,
        font_style=FontStyle.BOLD,
        font="Liberation Sans",
        # (openscad's center=true doesn't seem to do anything for text,
        # the locations specified in the original code are for minimum alignment)
        align=Align.MIN,
    ),
    amount=2,
)
base_result -= Location((-18, 51, 0.6), (180, 0, 0)) * extrude(
    Text(
        "PRUSA",
        font_size=11 * text_scale_constant,
        font_style=FontStyle.BOLD,
        font="Liberation Sans",
        align=Align.MIN,
    ),
    amount=2,
)
base_result -= Location((-66, 40.5, -0.4)) * cube([45, 1.6, 1])
base_result -= Location((-66, 41.3, -0.4)) * cylinder(h=1, r1=0.8)
base_result -= Location((-21, 41.3, -0.4)) * cylinder(h=1, r1=0.8)

# Front cleanup
base_result -= Location((-100, -64.6, 0)) * cube([200, 50, 50])

# X sign on reset button
base_result -= Location((63, 34, -1), (0, 0, 45)) * cube([2, 8, 2])
base_result -= Location((57.5, 35.5, -1), (0, 0, -45)) * cube([2, 8, 2])

# Corners
base_result -= Location((74.05, -5, -2.7), (0, 35, 0)) * cube([7, 80, 7])
base_result -= Location((-82.8, -5, -1), (0, 55, 0)) * cube([7, 80, 7])
base_result -= Location((-82, 58.5, -5), (55, 0, 0)) * cube([200, 7, 7])
base_result -= Location((-77, 51, -4), (0, 0, 45)) * cube([8, 8, 50])
base_result -= Location((78, 51, -4), (0, 0, 45)) * cube([8, 8, 50])
base_result -= Location((78, -19, -4), (0, 0, 45)) * cube([5, 5, 50])
base_result -= Location((-77, -19, -4), (0, 0, 45)) * cube([5, 5, 50])

# LCD corners
base_result -= Location((-52.5, 9.5, -5.2), (45, 0, 0)) * cube([80, 5, 5])  # LCD window
base_result -= Location((-52.5, 37, -5.2), (45, 0, 0)) * cube([80, 5, 5])  # LCD window
base_result -= (
    Location((0, 0, 0), (32, 0, 0))
    * Location((-78, -9.1, -4), (0, 0, 45))
    * cube([6, 6, 50])
)
base_result -= (
    Location((0, 0, 0), (32, 0, 0))
    * Location((79, -9.1, -4), (0, 0, 45))
    * cube([6, 6, 50])
)
base_result -= Location((-100, -40, -50)) * cube([200, 50, 50])

# Version
base_result -= (
    # build123d's rotation order is different from OpenSCADs
    Location((-73, 15, 4), (0, 0, 90))
    * Location((0, 0, 0), (90, 0, 0))
    * extrude(
        Text(
            "R7",
            font_size=7 * text_scale_constant,
            font_style=FontStyle.BOLD,
            font="Liberation Sans",
            align=Align.MIN,
        ),
        amount=2,
    )
)

# SD card window support
sd_card_window_support = Location((-76.5, 15, 16.7)) * cube([1, 5, 4.1])
sd_card_window_support += Location((-76.5, 25, 16.7)) * cube([1, 5, 4.1])

result_printable = base_result + sd_card_window_support

clip_support_mask = Location((-4, -10.7, 14.5)) * cube([10, 10, 3])
result_final = base_result - clip_support_mask

results = {"printable": result_printable, "post-processed": result_final}

if "show_object" in locals():
    show_object(result_final)
