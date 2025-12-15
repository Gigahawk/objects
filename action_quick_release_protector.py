"""Joint Protector for Action Quick Release joint used in the Action ACTBJ09"""

from build123d import *
from bd_warehouse.thread import Thread

from math import tan, radians


outer_dia = 21.5

protection_ring_dia = 24.0
protection_ring_height = 6
protection_ring_upper_chamfer_len = 2
# HACK: To compensate for loft cut
protection_ring_extra = 0.2

_shoulder_dia = 8
_shoulder_length = 9.15
shoulder_tol = 0.2
shoulder_dia = _shoulder_dia + shoulder_tol
shoulder_length = _shoulder_length + shoulder_tol

thread_maj_dia = (5 / 16) * 25.4
thread_min_dia = 6.9
thread_tip_width = 0.75
thread_root_width = 1.4

# Measures roughly 2.575mm between threads, using closest imperial conversion.
thread_pitch = (3 / 32) * 25.4
thread_length = 8
thread_tol = 0.1

_lead_in_length = 9.6
lead_in_length_tol = 1
lead_in_length = _lead_in_length + lead_in_length_tol
_lead_in_dia = 6.45
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

total_length = shoulder_length + thread_length + lead_in_length + top_thickness

top_chamfer_loft_top_dia = outer_dia - 2 * top_loft_chamfer_inset
top_chamfer_loft_bot_dia = top_chamfer_loft_top_dia + 2 * (
    total_length / tan(radians(top_loft_chamfer_angle))
)

# OrcaSlicer fork provides a brick layers option with overextrusion for better strength.
# This seems to screw up the internal dimensions.
# Compensating for 1.1 flow ratio on even loops
# brick_layers_comp = 0.4  # seems to be fine straight off the build plate but a little too tight after washing?
brick_layers_comp = 0.6
shoulder_dia += brick_layers_comp
thread_maj_dia += brick_layers_comp
thread_min_dia += brick_layers_comp
lead_in_dia += brick_layers_comp


_female_thread = Thread(
    apex_radius=thread_min_dia / 2 + thread_tol,
    apex_width=thread_tip_width,
    root_radius=thread_maj_dia / 2 + thread_tol,
    root_width=thread_root_width,
    pitch=thread_pitch,
    length=thread_length,
    end_finishes=("fade", "fade"),
)

with BuildPart() as female:
    with BuildSketch():
        Circle(outer_dia / 2)
        Circle(shoulder_dia / 2, mode=Mode.SUBTRACT)
    extrude(amount=shoulder_length)
    top_face = female.faces().sort_by(Axis.Z)[-1]
    with Locations((0, 0, shoulder_length)):
        add(_female_thread)
    with BuildSketch(top_face):
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
    chamfer_len1 = 0.7259792226230017
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

    with BuildSketch() as protection_ring_sketch:
        Circle(protection_ring_dia / 2)
        Circle(outer_dia / 2 - protection_ring_extra, mode=Mode.SUBTRACT)
    extrude(amount=protection_ring_height)
    protection_edges = (
        female.edges(select=Select.LAST)
        .filter_by(GeomType.CIRCLE)
        .filter_by(lambda x: x.radius == protection_ring_dia / 2)
    )
    top_edge = protection_edges.sort_by(Axis.Z, reverse=True)[0]
    bot_edge = protection_edges.sort_by(Axis.Z)[0]
    bot_chamfer = (protection_ring_dia - outer_dia) / 2
    # top_chamfer1 = female.part.max_fillet([top_edge], max_iterations=100)
    # print(f"top_chamfer1: {top_chamfer1}")
    top_chamfer1 = 1.2295599156351562
    chamfer(
        objects=bot_edge,
        length=bot_chamfer,
    )
    chamfer(
        objects=top_edge,
        length=protection_ring_upper_chamfer_len,
        length2=top_chamfer1,
    )


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
