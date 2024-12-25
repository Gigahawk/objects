"""Phone mount for Tempo Fitness Magnetic Exercise Bike (84-0199-8)

Replaces the included computer module.
"""

from math import tan, cos, radians
from build123d import *

tol = 0.15

mount_thickness = 2
mount_max_length = 75
mount_retention_width = 2
mount_retention_depth = 2

_pipe_outer_dia = 50.2
pipe_outer_dia = _pipe_outer_dia + tol
pipe_cut_angle = 45
pipe_cut_depth = pipe_outer_dia * tan(radians(pipe_cut_angle))
pipe_cut_hypot = pipe_outer_dia / cos(radians(pipe_cut_angle))

mount_outer_dia = pipe_outer_dia + mount_thickness*2
mount_retention_inner_dia = _pipe_outer_dia - mount_retention_width*2
phone_stand_width = 140
phone_stand_height = 80
phone_stand_thickness = 4
phone_thickness = 14
phone_stand_chin_height = 5
cable_width = 15


with BuildPart() as shell:
    Cylinder(
        mount_outer_dia/2, mount_max_length,
        align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    # Hack: an extra edge is formed if we put this sketch in the center
    with BuildSketch(Plane.XZ.offset(-mount_outer_dia/2)) as side_prof:
        Rectangle(mount_outer_dia, mount_max_length, align=(Align.CENTER, Align.MIN))
        with BuildLine():
            Polyline(
                [
                    (-mount_outer_dia/2, mount_max_length),
                    (mount_outer_dia/2, mount_max_length),
                    (-mount_outer_dia/2, mount_max_length - pipe_cut_depth),
                ],
                close=True,
            )
        make_face(mode=Mode.SUBTRACT)
    extrude(amount=mount_outer_dia, mode=Mode.INTERSECT, )

with BuildPart() as mount_pipe:
    add(shell)
    Cylinder(
        pipe_outer_dia/2, mount_max_length,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
        mode=Mode.SUBTRACT
    )

with BuildPart() as phone_stand:
    add(shell)
    Cylinder(
        # Hack: OCC tol seems to cause this cyl to not be tall enough
        _pipe_outer_dia/2, mount_max_length + 10,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
        mode=Mode.INTERSECT
    )
    Cylinder(
        mount_retention_inner_dia/2, mount_max_length,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
        mode=Mode.SUBTRACT
    )
    # Hack: an extra edge is formed if we put this sketch in the center
    with BuildSketch(Plane.XZ.offset(-mount_outer_dia/2)) as side_prof:
        Rectangle(
            mount_outer_dia, mount_max_length - mount_retention_depth,
            align=(Align.CENTER, Align.MIN)
        )
        with BuildLine():
            Polyline(
                [
                    (-mount_outer_dia/2, mount_max_length - mount_retention_depth),
                    (mount_outer_dia/2, mount_max_length - mount_retention_depth),
                    (-mount_outer_dia/2, mount_max_length - pipe_cut_depth - mount_retention_depth),
                ],
                close=True,
            )
        make_face(mode=Mode.SUBTRACT)
    extrude(amount=mount_outer_dia, mode=Mode.SUBTRACT)
    mount_face = phone_stand.faces().sort_by(Axis.Z, reverse=True)[0]
    with BuildSketch(mount_face) as phone_mount:
        Rectangle(phone_stand_height, phone_stand_width)
    extrude(amount=phone_stand_thickness)
    phone_face = phone_stand.faces().sort_by(Axis.Z, reverse=True)[0]
    phone_side_face = phone_stand.faces().sort_by(Axis.Y)[0]
    with BuildSketch(phone_side_face.offset(-phone_stand_width/2)) as phone_holder_chin:
        with Locations((phone_stand_height/2, -phone_stand_thickness/2)):
            Rectangle(
                phone_stand_thickness, phone_thickness + phone_stand_thickness,
                align=(Align.MAX, Align.MAX)
            )
        with Locations((
            phone_stand_height/2 - phone_stand_thickness,
            -phone_stand_thickness/2 - phone_thickness
        )):
            Rectangle(
                phone_stand_chin_height, phone_stand_thickness,
                align=(Align.MAX, Align.MAX)
            )
    extrude(amount=phone_stand_width/2, both=True)
    extrude(phone_holder_chin.sketch, amount=cable_width/2, both=True, mode=Mode.SUBTRACT)

results = {
    "pipe": mount_pipe.part,
    "stand": phone_stand.part,
}

if __name__ == "__main__":
    try:
        from ocp_vscode import *
        show_all(reset_camera=Camera.KEEP)
    except ImportError:
        pass

