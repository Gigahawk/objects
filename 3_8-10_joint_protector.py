"""Joint Protector for 3/8-10 cue joints"""

from build123d import *
from bd_warehouse.thread import IsoThread

from math import tan, radians


outer_dia = 21.5

thread_maj_dia = (3 / 8) * 25.4

thread_pitch = (1 / 10) * 25.4
thread_length = 12
thread_tol = 0.1

_lead_in_length = 11
lead_in_length_tol = 1
lead_in_length = _lead_in_length + lead_in_length_tol
_lead_in_dia = 6.4
lead_in_dia_tol = 0.2
lead_in_dia = _lead_in_dia + lead_in_dia_tol
lead_in_chamfer_depth = 4

top_thickness = 15
top_loft_chamfer_inset = 1.5
top_loft_chamfer_angle = 60
top_secondary_chamfer_len = 1

notch_start = 4
notch_height = 1
notch_depth = 0.8
notch_count = 3
notch_offset = 2.5

num_faces = 6

total_length = thread_length + lead_in_length + top_thickness

top_chamfer_loft_top_dia = outer_dia - 2 * top_loft_chamfer_inset
top_chamfer_loft_bot_dia = top_chamfer_loft_top_dia + 2 * (
    total_length / tan(radians(top_loft_chamfer_angle))
)

# OrcaSlicer fork provides a brick layers option with overextrusion for better strength.
# This seems to screw up the internal dimensions.
# Compensating for 1.1 flow ratio on even loops
# brick_layers_comp = 0.4  # seems to be fine straight off the build plate but a little too tight after washing?
brick_layers_comp = 0.6
thread_maj_dia += brick_layers_comp
lead_in_dia += brick_layers_comp


_female_thread = IsoThread(
    major_diameter=thread_maj_dia,
    pitch=thread_pitch,
    external=False,
    length=thread_length,
    end_finishes=("fade", "fade"),
)

with BuildPart() as female:
    add(_female_thread)
    with BuildSketch():
        Circle(outer_dia / 2)
        Circle(thread_maj_dia / 2 + thread_tol, mode=Mode.SUBTRACT)
    extrude(amount=thread_length)
    top_face = female.faces().sort_by(Axis.Z)[-1]
    with BuildSketch(top_face):
        Circle(outer_dia / 2)
        Circle(lead_in_dia / 2, mode=Mode.SUBTRACT)
    extrude(amount=lead_in_length - lead_in_dia / 2)
    inner_edge = (
        female.edges()
        .filter_by(GeomType.CIRCLE)
        .sort_by(lambda x: x.radius)[:2]
        .sort_by(Axis.Z)[0]
    )
    # chamfer_len1 = female.part.max_fillet([inner_edge], max_iterations=100)
    # print(chamfer_len1)
    chamfer_len1 = 1.5017881058252787
    chamfer(
        objects=inner_edge,
        length=lead_in_chamfer_depth,
        length2=chamfer_len1,
    )
    top_face = female.faces().sort_by(Axis.Z)[-1]
    with BuildSketch(top_face):
        Circle(outer_dia / 2)
    extrude(amount=top_thickness + lead_in_dia / 2)
    with Locations((0, 0, top_face.center().Z)):
        Sphere(radius=lead_in_dia / 2, mode=Mode.SUBTRACT)

    top_face = female.faces().sort_by(Axis.Z)[-1]
    bot_face = female.faces().sort_by(Axis.Z)[0]
    with BuildSketch(top_face) as loft_top:
        RegularPolygon(
            side_count=num_faces,
            radius=outer_dia / 2,
            major_radius=True,
        )
    with BuildSketch(bot_face) as loft_bot:
        RegularPolygon(
            side_count=num_faces,
            radius=outer_dia / 2,
            major_radius=False,
        )
    loft(sections=[loft_top.sketch, loft_bot.sketch], mode=Mode.INTERSECT)
    with BuildSketch(top_face) as chamfer_loft_top:
        RegularPolygon(
            side_count=num_faces,
            radius=top_chamfer_loft_top_dia / 2,
            major_radius=True,
        )
    with BuildSketch(bot_face) as chamfer_loft_bot:
        RegularPolygon(
            side_count=num_faces,
            radius=top_chamfer_loft_bot_dia / 2,
            major_radius=True,
        )
    loft(
        sections=[chamfer_loft_top.sketch, chamfer_loft_bot.sketch], mode=Mode.INTERSECT
    )

    top_face = female.faces().sort_by(Axis.Z)[-1]
    chamfer(top_face.edges(), length=top_secondary_chamfer_len)

    with BuildSketch(Plane.XZ) as notch_sketch:
        point = Vector(outer_dia / 2, top_face.center().Z - notch_start)
        with Locations(point):
            with GridLocations(
                x_spacing=0,
                y_spacing=-notch_offset,
                x_count=1,
                y_count=notch_count,
                align=Align.MIN,
            ):
                Rectangle(width=notch_depth, height=notch_height, align=Align.MAX)
    revolve(axis=Axis.Z, mode=Mode.SUBTRACT)


results = {
    "female": female.part,
}

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
        )
    except ImportError:
        pass
