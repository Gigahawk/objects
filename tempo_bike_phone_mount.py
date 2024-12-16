"""Phone mount for Tempo Fitness Magnetic Exercise Bike (84-0199-8)

Replaces the included computer module.
"""

from math import tan, cos, radians
from build123d import *

tol = 0.1

mount_thickness = 2
mount_max_length = 75

pipe_outer_dia = 50.2 + tol
pipe_cut_angle = 45
pipe_cut_depth = pipe_outer_dia * tan(radians(pipe_cut_angle))
pipe_cut_hypot = pipe_outer_dia / cos(radians(pipe_cut_angle))
print(pipe_outer_dia)
print(pipe_cut_depth)
print(pipe_cut_hypot)

with BuildPart() as pipe:
    Cylinder(
        pipe_outer_dia/2, mount_max_length,
        align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    # Hack: an extra edge is formed if we put this sketch in the center
    with BuildSketch(Plane.XZ.offset(-pipe_outer_dia/2)) as side_prof:
        Rectangle(pipe_outer_dia, mount_max_length, align=(Align.CENTER, Align.MIN))
        with BuildLine():
            Polyline(
                [
                    (-pipe_outer_dia/2, mount_max_length),
                    (pipe_outer_dia/2, mount_max_length),
                    (-pipe_outer_dia/2, mount_max_length - pipe_cut_depth),
                ],
                close=True,
            )
        make_face(mode=Mode.SUBTRACT)
    extrude(amount=pipe_outer_dia, mode=Mode.INTERSECT, )

with BuildPart() as mount:
    # HACK: include top surface for thickening otherwise the angled top face
    # is not correct
    pipe_faces = ShapeList([
        f for f in pipe.part.shell().faces()
        if f.center_location.position.Z != 0
    ])
    pipe_shell = Shell(pipe_faces)
    add(pipe_shell.thicken(mount_thickness))
    # HACK: remove top surface to replace with phone stand surface
    top_face = mount.faces().sort_by(Axis.Z, reverse=True)[0]
    with BuildSketch(top_face):
        Rectangle(pipe_cut_hypot*2, pipe_cut_hypot*2)
    extrude(amount=-mount_thickness, mode=Mode.SUBTRACT)
    top_face = mount.faces().sort_by(Axis.Z, reverse=True)[0]

result = mount.part

if __name__ == "__main__":
    try:
        from ocp_vscode import *
        show_all()
    except ImportError:
        pass

