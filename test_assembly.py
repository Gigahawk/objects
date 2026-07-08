"""Simple assembly example"""

import copy

from build123d import *


pcb_thickness = 1.6
pcb_length = 50
pcb_width = 20
housing_gap = 1
housing_wall_thickness = 2
housing_depth = 5
housing_length = pcb_length + 2 * housing_gap + 2 * housing_wall_thickness
housing_width = pcb_width + 2 * housing_gap + 2 * housing_wall_thickness
cavity_length = pcb_length + 2 * housing_gap
cavity_width = pcb_width + 2 * housing_gap
window_length = 30
window_width = 15

with BuildPart() as pcb:
    Box(pcb_length, pcb_width, pcb_thickness)
    bottom = pcb.faces().sort_by(Axis.Z)[0]
    top = pcb.faces().sort_by(Axis.Z)[-1]
    with BuildSketch(bottom):
        Text("BOT", font_size=10)
    extrude(amount=-pcb_thickness / 10, mode=Mode.SUBTRACT)
    with BuildSketch(top):
        Text("TOP", font_size=10)
    extrude(amount=-pcb_thickness / 10, mode=Mode.SUBTRACT)
    RigidJoint(label="pcb_top", joint_location=top.center_location)

with BuildPart() as housing:
    with BuildSketch():
        Rectangle(housing_length, housing_width)
    extrude(amount=housing_wall_thickness + housing_depth)
    top = housing.faces().sort_by(Axis.Z)[-1]
    with BuildSketch(top):
        Rectangle(cavity_length, cavity_width)
    extrude(amount=-housing_depth, mode=Mode.SUBTRACT)

    # bottom window
    with BuildSketch():
        Rectangle(window_length, window_width)
    extrude(amount=housing_wall_thickness, mode=Mode.SUBTRACT)
    inner_wall = housing.faces().filter_by(Axis.Z).sort_by(Axis.Z)[1]
    RigidJoint(
        label="housing_inner",
        joint_location=-inner_wall.center_location * Location((0, 0, 0), (0, 0, 180)),
    )

housing.joints["housing_inner"].connect_to(pcb.joints["pcb_top"])
asm = Compound(children=[copy.copy(pcb.part), copy.copy(housing.part)])

results = {
    "pcb": pcb.part,
    "housing": housing.part,
    # "asm": asm,
}

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
            render_joints=True,
        )
    except ImportError:
        pass
