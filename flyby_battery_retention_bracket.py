"""Battery retention bracket for the Flyby Accugun Pro"""

from build123d import *

width = 15.7
length = 75.25
thickness = 2.65
tab_length = 16
fillet_rad = 4
drop_distance = 7.5 - thickness

corner_chamfer = 2.5

hole_dia = 3.9
hole_distance = 59.5 + hole_dia


with BuildPart() as bracket:

    with BuildSketch() as profile_sketch:
        with BuildLine(mode=Mode.PRIVATE):
            l1 = Line((-length/2, 0), (-length/2 + tab_length, 0))
            l2 = Line(l1 @ 1, (l1 @ 1) + (drop_distance, -drop_distance))
            l3 = Line(l2 @ 1, (0, -drop_distance))
        with BuildLine() as profile_line:
            half_line = FilletPolyline(
                [l1 @ 0, l2 @ 0, l3 @0, l3 @1],
                radius=fillet_rad
            )
            mirror(half_line, Plane.YZ)
            offset(
                amount=thickness, side=Side.RIGHT,
                closed=True, kind=Kind.TANGENT)
        make_face()
    extrude(amount=width/2, both=True)

    with BuildSketch(Plane.XZ) as hole_sketch:
        with Locations([(-hole_distance/2, 0), (hole_distance/2, 0)]):
            Circle(hole_dia/2)
    extrude(until=Until.LAST, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XZ) as chamfer_sketch:
        Rectangle(length, width)
        chamfer(chamfer_sketch.vertices(), length=corner_chamfer)
    extrude(until=Until.LAST, mode=Mode.INTERSECT)

result = bracket.part

if __name__ == "__main__":
    if "show_object" in locals():
        show_object(bracket)

    try:
        from ocp_vscode import *
        show_all()
    except ImportError:
        pass

