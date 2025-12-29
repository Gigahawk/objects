from build123d import *

dlp_offset = 10

pole_hook_height = 40
pole_hook_inner_dia = 5
pole_hook_thickness = 2
pole_thickness = 7
pole_width = 7
pole_mount_offset = 27
pole_tol = 0.1
pole_nut_height = 27
pole_height = pole_hook_height + pole_hook_inner_dia + pole_thickness / 2
pole_hook_outer_dia = pole_hook_inner_dia + 2 * pole_hook_thickness


with BuildPart() as pole:
    with BuildLine() as pole_path:
        Polyline(
            [
                (-pole_mount_offset, 0, 0),
                (-pole_mount_offset, 0, pole_height),
                (dlp_offset + pole_hook_outer_dia / 2, 0, pole_height),
            ],
        )
        _pole_fillet_corner = (
            pole_path.vertices().sort_by(Axis.Z, reverse=True)[0:2].sort_by(Axis.X)
        )[0]
        fillet(_pole_fillet_corner, radius=10)
    with BuildSketch() as pole_profile:
        with Locations((-pole_mount_offset, 0)):
            Rectangle(pole_thickness, pole_width, align=Align.CENTER)
    sweep(sections=pole_profile.sketch, path=pole_path.line)

    pole_front_face = pole.faces().filter_by(Axis.X).sort_by(Axis.X)[-1]

    # HACK: I have no idea why, but when hook_blank_sketch is extruded,
    # it causes an the bottom of the pole to be extended by a little bit?
    # even though we are extruding in a completely different area.
    # Cache this face ahead of time so we can cut off the extra length
    # later.
    pole_bot_face = pole.faces().filter_by(Axis.Z).sort_by(Axis.Z)[0]
    with BuildSketch(pole_front_face) as hook_blank_sketch:
        Rectangle(pole_thickness, pole_width)
    # This extrude call makes the bottom of the pole get extended for some reason?
    # extrude(amount=-pole_hook_outer_dia)

    # The extra extension can of course just be removed afterwards but hacky
    # with BuildSketch(pole_bot_face) as _pole_hack_fixup_sketch:
    #    Rectangle(pole_width, pole_thickness)
    # extrude(amount=100, mode=Mode.SUBTRACT)


if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
            render_joints=True,
        )
    except ImportError:
        pass
