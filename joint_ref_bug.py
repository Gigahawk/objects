"""Demo of weird joint behavior when parts are modified after joints are assigned"""

import copy
from build123d import *


with BuildPart() as parent:
    Box(10, 10, 10, align=Align.CENTER)
    bot_face = parent.faces().sort_by(Axis.Z)[0]
    RigidJoint(label="parent", joint_location=Location(bot_face.center()))
    parent.part.color = Color("red")

with BuildPart() as child:
    Box(8, 20, 8, align=Align.CENTER)
    top_face = child.faces().sort_by(Axis.Z)[-1]
    RigidJoint(label="child", joint_location=Location(top_face.center()))
    # Not sure if nesting like this is relevant
    with BuildPart(mode=Mode.PRIVATE) as cutout_tool:
        Cylinder(2.5, 5, align=Align.CENTER)
    child.part.color = Color("green")

# If uncommented this line makes the connect_to line move `child_cutout`
# instead of child.
# `asm` will contain two cubes centered at the origin,
# the cube with a cylinder cutout will be moved to the bottom
# child_cutout = child.part - cutout_tool.part

# This line works as expected (`child_cutout` stays in the center, only `child` is moved)
child_cutout = copy.copy(child.part) - cutout_tool.part

child_cutout.color = Color("blue")

parent.part.joints["parent"].connect_to(child.part.joints["child"])

asm = Compound(children=[parent.part, child.part])

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
            render_joints=True,
        )
    except ImportError:
        pass
