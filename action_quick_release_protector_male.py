"""Joint Protector for 3/8-10 cue joints"""

from build123d import *
from bd_warehouse.thread import Thread

from math import tan, radians

# McMaster model has origin at center of all axes, head is at positive Z.
# Reorient to have the mating side of the head at origin facing positive Z.
_screw = import_step("res/91292A837_18-8_Stainless_Steel_Socket_Head_Screw.step")
_cyl_faces = _screw.faces().filter_by(GeomType.CYLINDER).sort_by(lambda x: x.radius, reverse=True)
_head = _cyl_faces[0]
head_radius = _head.radius
head_height = _head.edges().filter_by(GeomType.LINE)[0].length
# Shank is slightly larger than threads.
# Have to skip 2 faces since the head is comprised of 2 half cylindrical faces
_shank = _cyl_faces[2]
shank_radius = _shank.radius
_base_pos = _shank.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z)[-1].arc_center
# Move mating face to origin
_screw.move(Location(-_base_pos))
# Rotate screw to point up. Why is there move/moved but not rotate/rotated?
_screw = _screw.rotate(Axis.X, 180)
_screw_tip_pos = _screw.faces().filter_by(GeomType.PLANE).sort_by(Axis.Z)[-1].center().Z

screw_rad_tol = 0.1
screw_head_extra = 0.2
screw_tip_tol = 0.5

nut_height = 37

## McMaster model has origin at center of all axes, aligned to Y axis
_nut = import_step("res/97258A122_18-8_Stainless_Steel_Thin_Square_Nut.step")
# Rotate to align with Z axis
_nut = _nut.rotate(Axis.X, -90)
_nut_side_face = _nut.faces().filter_by(GeomType.PLANE).filter_by(Axis.X).sort_by(Axis.X)[0]
nut_width = abs(_nut_side_face.center().X) * 2
# Move to align bottom face with Z=0
_nut_bottom_face = _nut.faces().filter_by(GeomType.PLANE).sort_by(Axis.Z)[0]
nut_thickness = abs(_nut_bottom_face.center().Z) * 2
_nut.move(Location(-_nut_bottom_face.center()))
# Move to targeted height
_nut.move(Location(Vector(0, 0, nut_height)))

nut_width_tol = 0.2
nut_thickness_tol = 0.1

outer_dia = 21.5

protection_ring_dia = 24.0
protection_ring_height = 6
protection_ring_upper_chamfer_len = 2
# HACK: To compensate for loft cut
protection_ring_extra = 0.2

_shoulder_dia = 8
_shoulder_length = 9.15
shoulder_tol = 0.1
shoulder_dia = _shoulder_dia - shoulder_tol
shoulder_length = _shoulder_length - shoulder_tol


thread_maj_dia = (5 / 16) * 25.4
thread_min_dia = 6.9
thread_tip_width = 0.75
thread_root_width = 1.4

# Measures roughly 2.575mm between threads, using closest imperial conversion.
thread_pitch = (3 / 32) * 25.4
thread_length = 8
thread_tol = 0.1

thread_inset = 4
side_wall_thickness = 4

top_thickness = 25
top_loft_chamfer_inset = 1.5
top_loft_chamfer_angle = 60
top_secondary_chamfer_len = 1

notch_start = 4
notch_height = 1
notch_depth = 0.8
notch_count = 3
notch_offset = 2.5

num_faces = 6

total_length = thread_length + top_thickness

top_chamfer_loft_top_dia = outer_dia - 2 * top_loft_chamfer_inset
top_chamfer_loft_bot_dia = top_chamfer_loft_top_dia + 2 * (
    total_length / tan(radians(top_loft_chamfer_angle))
)

_male_thread = Thread(
    apex_radius=thread_maj_dia / 2 - thread_tol,
    apex_width=thread_tip_width,
    root_radius=thread_min_dia / 2 - thread_tol,
    root_width=thread_root_width,
    pitch=thread_pitch,
    length=thread_length,
    end_finishes=("fade", "fade"),
)
thread_min_dia = _male_thread.root_radius * 2


with BuildPart() as male:
    # Head cover
    with BuildSketch():
        Circle(thread_min_dia/2)
    extrude(amount=-(head_height + screw_head_extra))
    bottom_edge = male.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z)[0]
    with BuildSketch():
        Circle(head_radius + screw_rad_tol)
    extrude(amount=-(head_height + screw_head_extra), mode=Mode.SUBTRACT)
    #bottom_fillet = male.part.max_fillet([bottom_edge], max_iterations=100)
    #print(f"bottom_fillet: {bottom_fillet}")
    bottom_fillet = 0.9939773011714809
    fillet(objects=bottom_edge, radius=bottom_fillet)

    # Threaded portion
    with BuildSketch():
        Circle(thread_min_dia/2)
        Circle(shank_radius + screw_rad_tol, mode=Mode.SUBTRACT)
    extrude(amount=thread_length)
    add(_male_thread)

    # Shoulder portion
    top_face = male.faces().sort_by(Axis.Z)[-1]
    with BuildSketch(top_face):
        # Avoid making it actually shoulder width.
        # Probably don't want a stress concentration inside the joint
        #Circle(shoulder_dia/2)
        Circle(thread_min_dia/2)
        Circle(shank_radius + screw_rad_tol, mode=Mode.SUBTRACT)
    extrude(amount=shoulder_length)

    # Outer portion
    top_face = male.faces().sort_by(Axis.Z)[-1]
    # Cache this for later
    bot_face = top_face
    with BuildSketch(top_face):
        Circle(outer_dia / 2)
        Circle(shank_radius + screw_rad_tol, mode=Mode.SUBTRACT)
    extrude(amount=nut_height - top_face.center().Z)

    # Hopefully putting a screw in the middle will prevent breakage completely
    # but just in case create a pocket to hopefully put the break point somewhere
    # away from the face of the cue joint
    with BuildSketch(top_face):
        Circle(outer_dia / 2 - side_wall_thickness)
        Circle(thread_min_dia/2, mode=Mode.SUBTRACT)
    extrude(amount=thread_inset, mode=Mode.SUBTRACT)

    top_face = male.faces().sort_by(Axis.Z)[-1]
    with BuildSketch(top_face):
        Circle(outer_dia / 2)
        Rectangle(
            width=nut_width + nut_width_tol,
            height=nut_width + nut_width_tol,
            mode=Mode.SUBTRACT,
        )
    extrude(amount=nut_thickness + nut_thickness_tol)

    top_face = male.faces().sort_by(Axis.Z)[-1]
    with BuildSketch(top_face):
        Circle(outer_dia / 2)
        Circle(shank_radius + screw_rad_tol, mode=Mode.SUBTRACT)
    remaining_length = _screw_tip_pos - top_face.center().Z
    extrude(amount=remaining_length + screw_tip_tol)

    top_face = male.faces().sort_by(Axis.Z)[-1]
    with BuildSketch(top_face):
        Circle(outer_dia / 2)
    extrude(amount=top_thickness)

    top_face = male.faces().sort_by(Axis.Z)[-1]
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
    # HACK: need to loft to end to avoid cutting thread
    tip_face = male.faces().sort_by(Axis.Z)[0]
    with BuildSketch(tip_face) as loft_tip:
        RegularPolygon(
            side_count=num_faces,
            radius=top_chamfer_loft_bot_dia / 2,
            major_radius=True,
        )
    loft(
        sections=[loft_top.sketch, loft_bot.sketch, loft_tip.sketch],
        ruled=True,
        mode=Mode.INTERSECT,
    )
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
        sections=[chamfer_loft_top.sketch, chamfer_loft_bot.sketch, loft_tip.sketch],
        ruled=True,
        mode=Mode.INTERSECT,
    )

    top_face = male.faces().sort_by(Axis.Z)[-1]
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

    with BuildSketch(bot_face) as protection_ring_sketch:
        Circle(protection_ring_dia / 2)
        Circle(outer_dia / 2 - protection_ring_extra, mode=Mode.SUBTRACT)
    extrude(amount=protection_ring_height)
    protection_edges = (
        male.edges(select=Select.LAST)
        .filter_by(GeomType.CIRCLE)
        .filter_by(lambda x: x.radius == protection_ring_dia/2)
    )
    top_edge = protection_edges.sort_by(Axis.Z, reverse=True)[0]
    bot_edge = protection_edges.sort_by(Axis.Z)[0]
    bot_chamfer = (protection_ring_dia - outer_dia) / 2
    #top_chamfer1 = male.part.max_fillet([top_edge], max_iterations=100)
    #print(f"top_chamfer1: {top_chamfer1}")
    top_chamfer1 = 1.2238885740475043

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
    "male": male.part,
}

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
        )
    except ImportError:
        pass
