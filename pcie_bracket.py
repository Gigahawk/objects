"""PCIe filler bracket

Based on
https://web.archive.org/web/20201112014246/http://read.pudn.com/downloads166/ebook/758109/PCI_Express_CEM_1.1.pdf
"""

from math import tan, radians
from build123d import *

full_height = 21.59
inner_length = 120.02
inner_tab_length = 11.43

main_length = 115.46
main_height = 18.42
main_lower_corner_depth = 3.08
main_lower_corner_height = 2.54
main_upper_corner_depth = 2.92
main_upper_corner_horizontal_length = 1.64

guide_cutout_width = 3.05
guide_cutout_depth = 4.19
guide_cutout_offset = 10.92

screw_hole_cutout_diameter = 4.42
screw_hole_cutout_vertical_offset = 18.42
screw_hole_cutout_horizontal_offset = 5.08

taper_width = 10.19
taper_offset = 4.12
taper_depth = 7.27

# Make thicker for printing
thickness = 2.0
taper_thickness = 1.0
taper_section_length = 4.11/tan(radians(45))

support_gap = 0.2

with BuildPart() as bracket:

    with BuildSketch() as profile_sketch:
        with BuildLine() as inner_profile:
            Line((0, inner_tab_length), (0, 0))
            Line((0, 0), (inner_length, 0))
            offset(
                amount=thickness, side=Side.RIGHT,
                closed=True, kind=Kind.TANGENT)
        make_face()
    extrude(amount=full_height)

    with BuildSketch(Plane.XZ) as lower_taper_sketch:
        with BuildLine() as path:
            Line(
                (inner_length, taper_offset),
                (inner_length, taper_offset - support_gap))
        with BuildLine() as profile:
            Line(
                (inner_length, taper_offset),
                (inner_length - taper_depth, taper_offset))
            PolarLine(
                (inner_length - taper_depth, taper_offset),
                length=full_height, angle=-135)
        sweep(sections=profile.wires(), path=path.wires()[0])
    extrude(until=Until.LAST, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XZ) as upper_taper_sketch:
        with BuildLine():
            Line(
                (inner_length, taper_offset + taper_width),
                (inner_length - taper_depth, taper_offset + taper_width))
            PolarLine(
                (inner_length - taper_depth, taper_offset + taper_width),
                length=full_height, angle=135)
            offset(amount=full_height, side=Side.RIGHT, closed=True)
        make_face()
    extrude(until=Until.LAST, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XZ) as main_top_cutout:
        with BuildLine():
            Line(
                (inner_length, main_height),
                (inner_length - main_length, main_height))
            offset(amount=full_height, side=Side.RIGHT, closed=True)
        make_face()
    extrude(until=Until.LAST, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XZ) as main_lower_corner:
        with BuildLine() as path:
            Line(
                (0, main_lower_corner_height),
                (0, main_lower_corner_height - support_gap))
        with BuildLine() as profile:
            Line(
                (-thickness, main_lower_corner_height),
                (main_lower_corner_depth, main_lower_corner_height))
            PolarLine(
                (main_lower_corner_depth, main_lower_corner_height),
                length=full_height, angle=-45)
        sweep(sections=profile.wires(), path=path.wires()[0])
    extrude(until=Until.FIRST, both=True, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XZ) as main_upper_corner:
        with BuildLine():
            PolarLine(
                (main_upper_corner_depth, full_height),
                length=main_upper_corner_horizontal_length,
                length_mode=LengthMode.HORIZONTAL, angle=-45)
            offset(amount=full_height, side=Side.LEFT, closed=True)
        make_face()
    extrude(until=Until.LAST, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.YZ) as guide_cutout:
        with BuildLine():
            Line(
                (inner_tab_length, guide_cutout_offset),
                (inner_tab_length - guide_cutout_depth, guide_cutout_offset))
            Line(
                (inner_tab_length - guide_cutout_depth, guide_cutout_offset),
                (inner_tab_length - guide_cutout_depth, guide_cutout_offset + guide_cutout_width))
            Line(
                (inner_tab_length, guide_cutout_offset + guide_cutout_width),
                (inner_tab_length - guide_cutout_depth, guide_cutout_offset + guide_cutout_width))
            offset(amount=support_gap, side=Side.RIGHT, closed=True)
        make_face()
    extrude(until=Until.FIRST, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.YZ) as screw_hole_cutout:
        SlotCenterPoint(
            (screw_hole_cutout_horizontal_offset, screw_hole_cutout_vertical_offset + full_height),
            point=(screw_hole_cutout_horizontal_offset, screw_hole_cutout_vertical_offset),
            height=screw_hole_cutout_diameter)
    extrude(until=Until.FIRST, mode=Mode.SUBTRACT)

    with BuildSketch() as taper_thinning:
        with BuildLine():
            Line(
                (inner_length, -taper_thickness),
                (inner_length - taper_depth, -taper_thickness),
            )
            Line(
                (inner_length - taper_depth, -taper_thickness),
                (
                    (
                        inner_length
                        - taper_depth
                        - taper_section_length
                    ),
                    -thickness
                )
            )
            offset(
                amount=thickness, side=Side.LEFT,
                closed=True, kind=Kind.TANGENT)
        make_face()
    extrude(until=Until.LAST, mode=Mode.SUBTRACT)

result = bracket.part

if __name__ == "__main__":
    if "show_object" in locals():
        show_object(bracket)

    try:
        from ocp_vscode import *
        show_all(reset_camera=Camera.KEEP)
    except ImportError:
        pass

