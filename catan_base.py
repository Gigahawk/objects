"""Catan base"""
from build123d import *
from math import sqrt, radians, cos, sin

outer_flat_dist = 79
inner_flat_dist = 57.92
lip_flat_dist = 64.72
taper_flat_dist = 69
outer_corner_rad = outer_flat_dist/2 * (2/sqrt(3))
settlement_dia = 15.5

magnet_slot_start = (2.82, 36.43)
magnet_slot_dia = 4
magnet_slot_angle = 11
# Magnets are 3mm in diameter
magnet_slot_clearance = 3.3
magnet_slot_bump_height = magnet_slot_dia - magnet_slot_clearance
magnet_slot_bump_length = 2.5
magnet_slot_bump_fillet = magnet_slot_bump_height/2 - 0.0001
# Arbitrary depth of cut for magnet slot
magnet_slot_depth = 10
# Each magnet is 6mm long
magnet_slot_width = 6*2 + 1

base_height = 6
lip_height = 4
taper_height = 0.89
taper_angle = 157.5 - 90
settlement_height = 5.25
plug_clearance = 0.15
plug_width_clearance = 0.3

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

    # Magnet access slot
    with BuildSketch(Plane.ZY) as slot:
        with Locations(Location(magnet_slot_start, magnet_slot_angle - 90)):
            SlotCenterPoint(
                point=(0, 0), height=magnet_slot_dia, center=(magnet_slot_depth/2, 0))
            with Locations((0, -magnet_slot_dia/2)):
                Rectangle(
                    magnet_slot_bump_length, magnet_slot_bump_height,
                    align=(Align.MIN, Align.MIN), mode=Mode.SUBTRACT)
            Circle(radius=magnet_slot_dia/2)
        # Hack to select the two right angle corners
        filter_axis = Axis(
            origin=(0, magnet_slot_start[1], magnet_slot_start[0]),
            direction=(0, -cos(radians(magnet_slot_angle)), sin(radians(magnet_slot_angle))))
        points = (
            slot.vertices().filter_by_position(
                axis=filter_axis,
                minimum=magnet_slot_bump_length - 0.5,
                maximum=magnet_slot_bump_length + 0.5,
            )
        )
        # 3D fillet doesn't work for some reason, handle in 2D
        fillet(points, radius=magnet_slot_bump_fillet)
    hole = extrude(amount=magnet_slot_width/2, both=True, mode=Mode.PRIVATE)
    with PolarLocations(0, 6):
        add(hole, mode=Mode.SUBTRACT)

    # Settlement slots
    with BuildSketch(Location((0, 0, settlement_height))) as circles:
        with PolarLocations(outer_corner_rad, 6):
            Circle(radius=settlement_dia/2)
    extrude(until=Until.LAST, mode=Mode.SUBTRACT)

with BuildPart() as plug:
    with BuildSketch(Plane.ZY) as plug_sketch:
        with Locations(Location(magnet_slot_start, magnet_slot_angle - 90)):
            Rectangle(
                magnet_slot_depth, magnet_slot_dia - plug_clearance,
                align=(Align.MIN, Align.CENTER))
            Circle(
                radius=(magnet_slot_dia + plug_clearance)/2,
                mode=Mode.SUBTRACT)
            with Locations((0, -magnet_slot_dia/2)):
                Rectangle(
                    magnet_slot_bump_length + plug_clearance/2,
                    magnet_slot_bump_height + plug_clearance/2,
                    align=Align.MIN, mode=Mode.SUBTRACT,
                )
            corners = plug_sketch.vertices().filter_by_position(
                axis=filter_axis,
                minimum=magnet_slot_bump_length + plug_clearance/2 - 0.5,
                maximum=magnet_slot_bump_length + plug_clearance/2 + 0.5,
            )
            fillet(corners, radius=magnet_slot_bump_fillet)
    extrude(amount=(magnet_slot_width - plug_width_clearance)/2, both=True)

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


results = {
    "base": base.part,
    "plug": plug.part,
}

if __name__ == "__main__":
    if "show_object" in locals():
        show_object(base)

    try:
        from ocp_vscode import *
        show_all(measure_tools=True)
    except ImportError:
        pass
