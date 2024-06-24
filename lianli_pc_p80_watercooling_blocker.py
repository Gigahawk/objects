"""Plug to block the water cooling tubing holes in the Lian Li PC P80 Case"""
from build123d import *
from math import tan, radians

hole_dia = 25.5
chassis_thickness = 1.5
interference = 0.1
detent_angle = 10
tolerance = 0.1
plate_dia = 27
plate_thickness = 1

_cyl_height = chassis_thickness + tolerance
_cyl_dia = hole_dia - tolerance
_detent_height = (tolerance + interference)/2/tan(radians(detent_angle))

with BuildPart() as plug:
    with BuildSketch():
        Circle(plate_dia/2)
    extrude(amount=plate_thickness)
    with BuildSketch(plug.faces().sort_by(Axis.Z)[-1]):
        Circle(_cyl_dia/2)
    extrude(amount=_cyl_height)
    with BuildSketch(plug.faces().sort_by(Axis.Z)[-1]):
        Circle(_cyl_dia/2)
    extrude(amount=_detent_height, taper=-detent_angle)
    with BuildSketch(plug.faces().sort_by(Axis.Z)[-1]):
        Circle((hole_dia + interference)/2)
    extrude(amount=_detent_height, taper=detent_angle)


result = plug.part

if __name__ == "__main__":
    try:
        from ocp_vscode import *
        show_all(reset_camera=Camera.KEEP, measure_tools=True)
    except ImportError:
        pass