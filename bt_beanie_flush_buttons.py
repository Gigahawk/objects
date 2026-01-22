"""Flush mount buttons for the Asiilovi Bluetooth Beanie

This is to avoid the buttons being accidentally pressed when worn under a helmet.

https://www.amazon.ca/ASIILOVI-Bluetooth-Double-Layer-Packaging-Thanksgiving/dp/B07L3BWW5W

Print setting recommendations:
- Layer height: 0.1mm
- First layer has very little area, print slowly for better adhesion (50% speed seems fine)
    - I've had good success with printing at 100% speed after the first layer, but watch
      the print to make sure the pushers don't get knocked off during the print.
- (optional) Ironing on top layer only for a better finish
"""

from build123d import *


button_dia = 6
button_depth = 1.8 - 0.85
backing_thickness = 0.7
backing_rib_width = 1
button_clearance_dia = 4.7
button_pusher_dia = 1.3
button_pusher_taper = 40
button_clearance_depth = 1
button_clearance_chamfer = 0.5


mic_punchout_dia = 3 * 2

screw_punchout_dia = 1.76 * 2

side_rib_length = 7.43
rib_fillet = 1.25
top_rib_height = 7.3
center_button_rib_length = 5.5
center_rib_offset = 0.5
top_circle_dia = 1.9 * 2
top_circle_hole_dia = 1.5

_button_locs = [
    (0, 0),
    (11.025, -2.005),
    (-11.025, -2.005),
]
button_locs = Locations(_button_locs)

mic_punchout_loc = Locations(
    (5.19, -3.02),
)

screw_punchout_locs = Locations(
    (-15.30, 0.932),
    (15.34, 0.732),
)

with BuildPart() as buttons:
    with BuildSketch() as button_sketch:
        with button_locs:
            Circle(button_dia / 2)
    extrude(amount=button_depth)

    with BuildSketch() as backing_sketch:
        with button_locs:
            Circle(button_dia / 2 + backing_rib_width)
        with mic_punchout_loc:
            Circle(mic_punchout_dia / 2, mode=Mode.SUBTRACT)
        with screw_punchout_locs:
            Circle(screw_punchout_dia / 2, mode=Mode.SUBTRACT)

        with BuildLine(mode=Mode.PRIVATE) as backing_rib_path_cons:
            side_lines = [PolarLine(c, side_rib_length, 90) for c in _button_locs[1:]]
            top_lines = [Line((0, top_rib_height), l @ 1) for l in side_lines]
            center_line_h = Line(
                (center_button_rib_length, center_rib_offset),
                (-center_button_rib_length, center_rib_offset),
            )
            center_lines_y = [
                Line(center_line_h @ idx, top_lines[idx] @ 0.5) for idx in range(2)
            ]

        with BuildLine() as backing_rib_path:
            top_line = FilletPolyline(
                [
                    side_lines[0] @ 0,
                    side_lines[0] @ 1,
                    (0, top_rib_height),
                    side_lines[1] @ 1,
                    side_lines[1] @ 0,
                ],
                radius=rib_fillet,
            )
            center_line = FilletPolyline(
                [
                    top_lines[0] @ 0.5,
                    center_line_h @ 0,
                    center_line_h @ 1,
                    top_lines[1] @ 0.5,
                ],
                radius=rib_fillet,
            )
        rib_top = offset(top_line, amount=backing_rib_width / 2)
        rib_center = offset(center_line, amount=backing_rib_width / 2)
        make_face(rib_top)
        make_face(rib_center)
        with Locations((0, top_rib_height)):
            Circle(top_circle_dia / 2)
            Circle(top_circle_hole_dia / 2, mode=Mode.SUBTRACT)

    extrude(amount=-backing_thickness)

    with BuildSketch(Plane.XY.offset(-backing_thickness)) as clearance_sketch:
        with button_locs:
            Circle(button_clearance_dia / 2)

    extrude(amount=button_clearance_depth, mode=Mode.SUBTRACT)

    clearance_edges = (
        buttons.edges(select=Select.LAST)
        .filter_by(GeomType.CIRCLE)
        .sort_by(Axis.Z, reverse=True)[:3]
    )
    chamfer(clearance_edges, length=button_clearance_chamfer)

    with BuildSketch(Plane.XY.offset(-backing_thickness)) as pusher_sketch:
        with button_locs:
            Circle(button_pusher_dia / 2)

    extrude(amount=button_clearance_depth, taper=-button_pusher_taper)


result = buttons.part

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(reset_camera=Camera.KEEP, render_joints=True)
    except ImportError:
        pass
