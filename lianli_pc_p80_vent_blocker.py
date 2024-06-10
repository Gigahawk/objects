"""Bracket to block the vents in a Lian Li PC P80 Case"""
from build123d import *

thickness = 4
blocker_width = 50
blocker_length = 160
hole_dia = 2.75
hole_vertical_sep = 18.7
hole_horizontal_sep = 6.3
hole_spacing = 131.3
fillet_rad = 10
# The actual vent holes on the case come really close
# to the screw holes, leave extra margin on the windowed
# variant to allow for clamping of a filter
#window_length = 125
#window_height = 38
window_length = 110
window_height = 34
window_fillet = 5

with BuildPart() as blocker_plate:
    with BuildSketch() as blocker_sketch:
        outer_plate = Rectangle(blocker_length, blocker_width)
        _inner_hole_rect = Rectangle(
            hole_spacing, hole_vertical_sep,
            mode=Mode.PRIVATE)
        _outer_hole_rect = Rectangle(
            hole_spacing + 2*hole_horizontal_sep, hole_vertical_sep,
            mode=Mode.PRIVATE)
        hole_points = ShapeList()
        for _rect in [_inner_hole_rect, _outer_hole_rect]:
            hole_points.extend(_rect.vertices())
        with Locations(hole_points):
            Circle(radius=hole_dia/2, mode=Mode.SUBTRACT)
        fillet(outer_plate.vertices(), radius=fillet_rad)
    extrude(amount=thickness)

with BuildPart() as window_plate:
    with BuildSketch() as window_sketch:
        add(blocker_sketch)
        window = Rectangle(
            window_length, window_height,
            mode=Mode.SUBTRACT)
        fillet(window.vertices(), radius=window_fillet)
    extrude(amount=thickness)

results = {
    "blocker": blocker_plate.part,
    "window": window_plate.part
}

if __name__ == "__main__":
    try:
        from ocp_vscode import *
        show_all(reset_camera=Camera.KEEP, measure_tools=True)
    except ImportError:
        pass