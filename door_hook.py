"""Hook that goes over the edge of a door"""

from build123d import *

# Thickness of the door
door_thickness = 20.5
# Thickness of the part
thickness = 5
# Length of the part that hangs behind the door
support_length = 10
width = 30
length = 40
hook_dia = 35

with BuildPart() as part:
    with BuildSketch() as sketch:
        with BuildLine() as path:
            l1 = Line((0, 0), (0, support_length))
            l2 = Line(l1@1, l1@1 + (door_thickness, 0))
            l3 = Line(l2@1, l2@1 - (0, length))
            l4 = TangentArc(l3@1, l3@1 + (hook_dia + thickness, 0), tangent=l3 % 1)
            offset(amount=thickness/4, side=Side.LEFT, closed=False, kind=Kind.TANGENT)
            offset(amount=thickness/4)
        make_face()
    extrude(amount=width)

result = part.part

if "show_object" in locals():
    show_object(part)


try:
    from ocp_vscode import *
    show(part)
except:
    pass