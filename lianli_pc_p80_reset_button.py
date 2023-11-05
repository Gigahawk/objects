"""Replacement reset button for a Lian Li PC P80 Case"""
from build123d import *

collar_dia = 9
collar_len = 15
collar_lip_dia = 11
collar_lip_thickness = 0.6
collar_hole_dia = 6.5
collar_retaining_dia = 8
collar_retaining_thickness = 1.2
bottom_thickness = 2
plate_thickness = 1.6
pusher_hole_dia = 4.2
spring_chamfer = (collar_hole_dia - pusher_hole_dia)/2 - 0.01

button_dia = 6.2
button_len = 5
pusher_dia = 4
pusher_len = 22 - button_len
pusher_retaining_dia = 3.5
pusher_retaining_thickness = 1.2

with BuildPart() as collar:
    with BuildSketch() as lip_sketch:
        Circle(collar_lip_dia/2)
    extrude(amount=collar_lip_thickness)
    lip_bottom = collar.faces().filter_by(GeomType.PLANE).sort_by(Axis.Z)[1]
    with BuildSketch(lip_bottom):
        Circle(collar_dia/2)
    extrude(amount=collar_len)
    with BuildSketch(Location((0, 0, plate_thickness))*lip_bottom):
        Circle(collar_dia/2)
        Circle(collar_retaining_dia/2, mode=Mode.SUBTRACT)
    extrude(amount=collar_retaining_thickness, mode=Mode.SUBTRACT)
    collar_bottom = collar.faces().sort_by(Axis.Z)[-1]
    with BuildSketch(collar_bottom):
        Circle(pusher_hole_dia/2)
    extrude(dir=(0, 0, -1), until=Until.LAST, mode=Mode.SUBTRACT)
    with BuildSketch(Location((0, 0, -bottom_thickness))*collar_bottom):
        Circle(collar_hole_dia/2)
    extrude(dir=(0, 0, -1), until=Until.LAST, mode=Mode.SUBTRACT)
    spring_face = collar.faces().filter_by(Axis.Z).sort_by(Axis.Z)[-2]
    spring_edge = spring_face.edges().filter_by(GeomType.CIRCLE).sort_by(SortBy.RADIUS)[0]
    chamfer(spring_edge, length=spring_chamfer)

with BuildPart() as button:
    with BuildSketch():
        Circle(button_dia/2)
    extrude(amount=button_len)
    with BuildSketch(button.faces().sort_by(Axis.Z)[-1]):
        Circle(pusher_dia/2)
    extrude(amount=pusher_len)
    with BuildSketch(collar_bottom):
        Circle(pusher_dia/2)
        Circle(pusher_retaining_dia/2, mode=Mode.SUBTRACT)
    extrude(amount=pusher_retaining_thickness, mode=Mode.SUBTRACT)



results = {
    "collar": collar.part,
    "button": button.part
}

if __name__ == "__main__":
    if "show_object" in locals():
        show_object(results["lian_li_power_button"])

    try:
        from ocp_vscode import *
        show_all()
    except:
        pass
