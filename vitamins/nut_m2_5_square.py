from pathlib import Path

from build123d import *

## McMaster model has origin at center of all axes, aligned to Y axis
_nut = import_step(Path(__file__).parent.parent / "res/97258A122_18-8_Stainless_Steel_Thin_Square_Nut.step")
# Rotate to align with Z axis
_nut = _nut.rotate(Axis.X, -90)

_nut_side_face = _nut.faces().filter_by(GeomType.PLANE).filter_by(Axis.X).sort_by(Axis.X)[0]
nut_width = abs(_nut_side_face.center().X) * 2
# Move to align bottom face with Z=0
_nut_bottom_face = _nut.faces().filter_by(GeomType.PLANE).sort_by(Axis.Z)[0]
nut_thickness = abs(_nut_bottom_face.center().Z) * 2
_nut.move(Location(-_nut_bottom_face.center()))

out = _nut

bottom_joint = RigidJoint(label="bottom", joint_location=Location((0,0,0)), to_part=out)

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
            render_joints=True
        )
    except ImportError:
        pass
