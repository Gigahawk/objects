from pathlib import Path

from build123d import *

# McMaster model has origin at center of all axes, head is at positive Z.
# Reorient to have the mating side of the head at origin facing positive Z.
_screw = import_step(Path(__file__).parent.parent / "res/91292A837_18-8_Stainless_Steel_Socket_Head_Screw.step")
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

out = _screw

head_bottom_joint = RigidJoint(
    label="head_bottom",
    joint_location=Location((0,0,0)),
    to_part=out
)

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
            render_joints=True
        )
    except ImportError:
        pass
