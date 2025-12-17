from pathlib import Path

from build123d import *

## McMaster model has origin at center of all axes, aligned to Z axis
_washer = import_step(
    Path(__file__).parent.parent
    / "res/91100A160_Zinc-Plated_Steel_Oversized_Washer.step"
)
# Move to align bottom face with Z=0
_washer_bottom_face = _washer.faces().filter_by(GeomType.PLANE).sort_by(Axis.Z)[0]
thickness = abs(_washer_bottom_face.center().Z) * 2
_washer.move(Location(-_washer_bottom_face.center()))

_washer_round_faces = (
    _washer.faces().filter_by(GeomType.CYLINDER).sort_by(lambda x: x.radius)
)
_washer_outer_face = _washer_round_faces[-1]
_washer_inner_face = _washer_round_faces[0]
outer_dia = _washer_outer_face.radius * 2
inner_dia = _washer_inner_face.radius * 2

out = _washer

bottom_joint = RigidJoint(
    label="bottom", joint_location=Location((0, 0, 0)), to_part=out
)

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(reset_camera=Camera.KEEP, render_joints=True)
    except ImportError:
        pass
