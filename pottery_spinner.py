"""Simple spinner for pottery trimming"""
from build123d import *

# 6700RS
bearing_outer_dia = 15
bearing_inner_dia = 10
bearing_width = 4
bearing_lip = 0.8
bearing_gap = 0.6

handle_dia = 27
handle_height = 40
handle_chamfer1 = 2
handle_chamfer2 = 1
handle_tol = -0.05
handle_bearing_chamfer = 0.6

spinner_dia = 35
spinner_thickness = 2*bearing_width
spinner_chamfer1 = 2
spinner_chamfer2 = 1
spinner_tol = 0.1
spinner_bearing_chamfer = 1

with BuildPart() as lower:
    Cylinder(
        spinner_dia/2, spinner_thickness,
        align=(Align.CENTER, Align.CENTER, Align.MAX)
    )
    top_face = lower.faces().sort_by(Axis.Z)[-1]
    spinner_edge = lower.faces().sort_by(Axis.Z)[0].edges()
    chamfer(spinner_edge, spinner_chamfer1, spinner_chamfer2)
    with BuildSketch(top_face):
        Circle((bearing_outer_dia + spinner_tol)/2)
    extrude(amount=-bearing_width, mode=Mode.SUBTRACT)
    chamfer_edge = lower.edges(Select.LAST).sort_by(Axis.Z)[-1]
    bearing_pocket_face = lower.faces(Select.LAST).sort_by(Axis.Z)[0]
    chamfer(chamfer_edge, spinner_bearing_chamfer)
    with BuildSketch(bearing_pocket_face):
        Circle((bearing_outer_dia/2 - bearing_lip))
    extrude(amount=-bearing_width/4, mode=Mode.SUBTRACT)

with BuildPart() as upper:
    Cylinder(
        (bearing_inner_dia - handle_tol)/2, bearing_width,
        align=(Align.CENTER, Align.CENTER, Align.MAX)
    )
    bearing_face = upper.faces().sort_by(Axis.Z)[-1]
    chamfer_edge = upper.faces().sort_by(Axis.Z)[0].edges()
    chamfer(chamfer_edge, spinner_bearing_chamfer)
    with BuildSketch(bearing_face):
        Circle((bearing_inner_dia/2 + bearing_lip))
    extrude(amount=bearing_gap)
    gap_face = upper.faces().sort_by(Axis.Z)[-1]
    with BuildSketch(gap_face):
        Circle((bearing_inner_dia/2 + bearing_lip))
    handle_face = upper.faces().sort_by(Axis.Z)[-1]
    with BuildSketch(handle_face):
        Circle(handle_dia/2)
    extrude(amount=handle_height)
    handle_chamfer_edge = upper.faces().sort_by(Axis.Z)[-1].edges()
    chamfer(handle_chamfer_edge, handle_chamfer1, handle_chamfer2)

results = {
    "lower": lower.part,
    "upper": upper.part
}

if __name__ == "__main__":
    try:
        from ocp_vscode import *
        show_all(
            reset_camera=Camera.KEEP,
        )
    except ImportError:
        pass