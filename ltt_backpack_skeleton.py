"""Ribbing to prevent tipping of the LTT Store Backpack"""

from math import tan, pi, cos
import cadquery as cq
from cq_warehouse.fastener import SocketHeadCapScrew, PlainWasher
import cq_warehouse.extensions

screw = SocketHeadCapScrew(
    size="M3-0.5", fastener_type="iso4762", length=20, simple=True)
washer = PlainWasher(size="M3", fastener_type="iso7093")

thickness = 20
width = 20
height = 100
length = 145
support_length = 100
fillet = 10
taper_angle = 30
taper_fillet = 3
tab_clearance = 0.1
counterbore_depth = 5
counterbore_clearance = 0.2
screw_length = 20
support_nut_depth1 = 7
support_nut_depth2 = 13
nut_width = 5.5
nut_thickness = 2.4
nut_clearance = 0.2

nut_rad_minor = (nut_width + nut_clearance)/2
nut_rad_major = nut_rad_minor/cos(pi/6)
tab_height = 2/3*thickness
tab_depth = width/2
screw_clearance = width/2
taper_length = tan((90 - taper_angle)*pi/180)*thickness
support_screw_depth = screw_length - (tab_depth - counterbore_depth) + 1


main_rib_points = [
    (0, 0),
    (length, 0),
    (length, height),
    (length - thickness, height - taper_length),
    (length - thickness, thickness),
    (thickness, thickness),
    (thickness, height - taper_length),
    (0, height)
]

support_rib_points = [
    (-tab_depth, (thickness - tab_height)/2),
    (0, (thickness - tab_height)/2),
    (0, 0),
    (support_length, 0),
    (support_length - taper_length, thickness),
    (0, thickness),
    (0, (thickness + tab_height)/2),
    (-tab_depth, (thickness + tab_height)/2)
]

support_nut_points = [
    (0, -nut_rad_major),
    ((nut_width + nut_clearance)/2, -cos(pi/3)*nut_rad_major),
    ((nut_width + nut_clearance)/2, 100),
    (-(nut_width + nut_clearance)/2, 100),
    (-(nut_width + nut_clearance)/2, -cos(pi/3)*nut_rad_major),
]

result = cq.Assembly()

main_rib = (
    cq.Workplane("XY").tag("base_plane")
    .polyline(main_rib_points).close().extrude(width)
    .edges("|Z and >Y").fillet(taper_fillet)
    .edges("|Z").fillet(fillet)
    .faces(">Z").workplane().center(length/2, thickness/2)
    .rect(width + tab_clearance, tab_height + tab_clearance)
    .cutBlind(-tab_depth)
    .workplaneFromTagged("base_plane").workplane(invert=True)
    .center(length/2, -thickness/2)
    .pushPoints([(-screw_clearance/2, 0), (screw_clearance/2, 0)])
    .circle(washer.washer_diameter/2 + counterbore_clearance)
    .cutBlind(-counterbore_depth)
    .workplaneFromTagged("base_plane")
    .workplane(invert=True, offset=-counterbore_depth)
    .center(length/2, -thickness/2)
    .pushPoints([(-screw_clearance/2, 0), (screw_clearance/2, 0)])
    .clearanceHole(
        fastener=screw, counterSunk=False,
        #baseAssembly=result
    )
)
main_rib.faces(">Z").tag("mating_face").end()
main_rib.faces("<Y").tag("bottom_face").end()
main_rib.faces("|X").faces(">>X[2]").tag("left_face").end()

support_rib = (
    cq.Workplane("XY").tag("base_plane")
    .polyline(support_rib_points).close().extrude(width)
)
support_rib.faces("|X").faces(">X").tag("mating_face").end()
support_rib.faces("<Y").tag("bottom_face").end()
support_rib.faces(">Z").tag("left_face").end()
support_rib = (
    support_rib
    .edges("|Z and >X").fillet(taper_fillet)
    .edges("|Z and >Y").edges(">X").fillet(fillet)
    .faces("<X").workplane()
    .center(-thickness/2, width/2)
    .pushPoints([(0, -screw_clearance/2), (0, screw_clearance/2)])
    .clearanceHole(fastener=screw, counterSunk=False, depth=support_screw_depth)
    .faces("<X").workplane(offset=-support_nut_depth1)
    .center(0, screw_clearance/2)
    .polyline(support_nut_points).close().cutBlind(nut_thickness)
    .faces("<X").workplane(offset=-support_nut_depth2)
    .center(0, -screw_clearance)
    .polyline(support_nut_points).close().cutBlind(nut_thickness)
)


result.add(main_rib, name="main_rib", color=cq.Color("green"))
result.add(support_rib, name="support_rib", color=cq.Color("blue"))
result.constrain("main_rib?mating_face", "support_rib?mating_face", "Axis")
result.constrain("main_rib?mating_face", "support_rib?mating_face", "PointInPlane")
result.constrain(
    "main_rib?bottom_face", "support_rib?bottom_face", "Axis", param=0)
result.constrain("main_rib?bottom_face", "support_rib?bottom_face", "PointInPlane")
result.constrain("main_rib?left_face", "support_rib?left_face", "Axis")
result.constrain(
    "main_rib?left_face", "support_rib?left_face", "PointInPlane",
    param=tab_clearance/2)

result.solve()

if "show_object" in locals():
    show_object(result, name="asm")