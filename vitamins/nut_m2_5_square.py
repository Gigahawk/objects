from pathlib import Path

from build123d import *

## McMaster model has origin at center of all axes, aligned to Y axis
_nut = import_step(
    Path(__file__).parent.parent
    / "res/97258A122_18-8_Stainless_Steel_Thin_Square_Nut.step"
)
# Rotate to align with Z axis
_nut = _nut.rotate(Axis.X, -90)

_nut_side_face = (
    _nut.faces().filter_by(GeomType.PLANE).filter_by(Axis.X).sort_by(Axis.X)[0]
)
nut_width = abs(_nut_side_face.center().X) * 2
# Move to align bottom face with Z=0
_nut_bottom_face = _nut.faces().filter_by(GeomType.PLANE).sort_by(Axis.Z)[0]
nut_thickness = abs(_nut_bottom_face.center().Z) * 2
_nut.move(Location(-_nut_bottom_face.center()))

hole_edge = _nut.edges().filter_by(GeomType.CIRCLE).sort_by_distance((0, 0, 0))[0]
hole_dia = hole_edge.radius * 2

out = _nut

bottom_joint = RigidJoint(
    label="bottom", joint_location=Location((0, 0, 0)), to_part=out
)


def build_cutout(
    width_tol=0.2,
    thickness_tol=0.2,
    with_bridge_helper=True,
    bridge_helper_hole_dia=hole_dia,
    layer_height=0.2,
):
    _width = nut_width + width_tol
    _thickness = nut_thickness + thickness_tol
    _align = (Align.CENTER, Align.CENTER, Align.MIN)
    with BuildPart() as nut_cutout:
        Box(_width, _width, _thickness, align=_align)
        if with_bridge_helper:
            Box(_width, bridge_helper_hole_dia, _thickness + layer_height, align=_align)
            Box(
                bridge_helper_hole_dia,
                bridge_helper_hole_dia,
                _thickness + 2 * layer_height,
                align=_align,
            )
    return nut_cutout.part


_cutout = build_cutout()

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(reset_camera=Camera.KEEP, render_joints=True)
    except ImportError:
        pass
