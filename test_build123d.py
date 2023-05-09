from build123d import *

length, width, thickness = 80.0, 60.0, 10.0
center_hole_dia = 22.0

with BuildPart() as part:
    Box(length, width, thickness)
    Cylinder(radius=center_hole_dia / 2, height=thickness, mode=Mode.SUBTRACT)

result = part.part

if "show_object" in locals():
    show_object(result)