"""Joint Protector for 3/8-10 cue joints"""

from build123d import *
from bd_warehouse.thread import IsoThread

from math import tan, radians


outer_dia = 20.8

protection_ring_dia = 23.0
protection_ring_height = 6
protection_ring_upper_chamfer_len = 2
# HACK: To compensate for loft cut
protection_ring_extra = 0.2

thread_maj_dia = (3 / 8) * 25.4

thread_pitch = (1 / 10) * 25.4
thread_length = 12
thread_tol = 0.6

_lead_in_length = 11
lead_in_length_tol = 1
lead_in_length = _lead_in_length + lead_in_length_tol
_lead_in_dia = 6.4
lead_in_dia_tol = 0.2
lead_in_dia = _lead_in_dia + lead_in_dia_tol
lead_in_chamfer_depth = 4

top_thickness = 30
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
    major_diameter=thread_maj_dia + thread_tol,
    pitch=thread_pitch,
    external=False,
    length=thread_length,
    end_finishes=("fade", "fade"),
    interference=2,  # HACK: fix broken overlap
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

    # Better since the chamfer can intersect the loft but causes geometry issues
    # with BuildSketch(Plane.YZ) as protection_ring_sketch:
    #    with BuildLine():
    #        Polyline([
    #            (outer_dia / 2 - protection_ring_extra, 0),
    #            (protection_ring_dia / 2, 0),
    #            (protection_ring_dia / 2, protection_ring_height),
    #            (outer_dia / 2 - protection_ring_extra, protection_ring_height),
    #        ])
    #    make_face()
    #    outer_corners = (
    #        protection_ring_sketch.vertices().sort_by(Axis.X, reverse=True)[:2]
    #    )
    #    nom_chamfer = (protection_ring_dia - outer_dia) / 2
    #    top_corner = outer_corners.sort_by(Axis.Y)[-1]
    #    bot_corner = outer_corners.sort_by(Axis.Y)[0]
    #    chamfer(bot_corner, length=nom_chamfer)
    #    chamfer(
    #        top_corner,
    #        length=protection_ring_upper_chamfer_len,
    #        length2=nom_chamfer + protection_ring_extra,
    #    )
    # revolve(axis=Axis.Z)
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
    top_chamfer1 = 1.046557026157684
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
