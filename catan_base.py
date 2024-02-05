"""Catan base"""
from build123d import *
from math import sqrt

outer_flat_dist = 79
inner_flat_dist = 57.92
lip_flat_dist = 64.72
taper_flat_dist = 69
outer_corner_rad = outer_flat_dist/2 * (2/sqrt(3))
settlement_dia = 15.5

magnet_slot_start = (2.82, 36.43)
magnet_slot_dia = 4
magnet_slot_angle = 11 - 90
# Each magnet is 6mm long
magnet_slot_width = 6*2 + 1


base_height = 6
lip_height = 4
taper_height = 0.89
taper_angle = 157.5 - 90
settlement_height = 5.25


with BuildPart() as base:
    # Frame base
    with BuildSketch():
        RegularPolygon(
            radius=outer_flat_dist/2, side_count=6, major_radius=False)
    extrude(amount=base_height)

    # Tapered section meeting art
    with BuildSketch(base.faces().sort_by(Axis.Z)[-1]):
        RegularPolygon(
            radius=taper_flat_dist/2, side_count=6, major_radius=False)
    extrude(amount=taper_height, taper=taper_angle)

    # Inner lip the art rests on
    with BuildSketch(Location((0, 0, lip_height))):
        RegularPolygon(
            radius=lip_flat_dist/2, side_count=6, major_radius=False)
    extrude(until=Until.LAST, mode=Mode.SUBTRACT)

    # Inner cutout for weight reduction/magnet access
    with BuildSketch():
        RegularPolygon(
            radius=inner_flat_dist/2, side_count=6, major_radius=False)
    extrude(until=Until.LAST, mode=Mode.SUBTRACT)

    # Magnet access
    with BuildSketch(Plane.ZY) as slot:
        with BuildLine(Plane.ZY):
            slot_center = PolarLine(start=magnet_slot_start, length=10, angle=magnet_slot_angle)
        SlotArc(arc=slot_center, height=magnet_slot_dia)
    hole = extrude(amount=magnet_slot_width/2, both=True, mode=Mode.PRIVATE)
    with PolarLocations(0, 6):
        add(hole, mode=Mode.SUBTRACT)

    # Settlement slots
    with BuildSketch(Location((0, 0, settlement_height))) as circles:
        with PolarLocations(outer_corner_rad, 6):
            Circle(radius=settlement_dia/2)
    extrude(until=Until.LAST, mode=Mode.SUBTRACT)

results = {
    "base": base.part,
}

if __name__ == "__main__":
    if "show_object" in locals():
        show_object(base)

    try:
        from ocp_vscode import *
        show_all()
    except:
        pass
