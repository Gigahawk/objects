"""Part from the Q4-Q5 of SOLIDWORKS CSWP Sample Exam

https://www.solidworks.com/certifications/mechanical-design-cswp-mechanical-design
"""

import logging

from math import tan, radians
from build123d import *

density = 0.0077  # g/mm^3

inputs = {
    "q4": {
        "A": 221,
        "B": 211,
        "C": 165,
        "D": 121,
        "E": 37,
    },
    "q5": {
        "A": 229,
        "B": 217,
        "C": 163,
        "D": 119,
        "E": 34,
    },
}

def build(A, B, C, D, E):
    X = A/3
    Y = B/3 + 15
    plate_thickness = 25
    wall_straight_length = 80
    wall_inner_rad = C - wall_straight_length
    wall_thickness = 15
    wall_height = 95 - plate_thickness
    total_wall_height = wall_height + plate_thickness
    cylinder_distance = C - wall_thickness/2
    cylinder_chamfer = 2
    cylinder_chamfer2 = cylinder_chamfer*tan(radians(30))
    cylinder_cut_radius = X/2 - 10
    cylinder_cut_height = 30
    cylinder_cut_offset = 30
    outer_fillet_radius = 10
    pocket_offset = -9
    pocket_depth = 5 - plate_thickness
    pocket_fillet_radius = 10


    with BuildPart() as part:
        # Main Base
        Box(A, B, plate_thickness, align=Align.MIN)
        main_workplane = Plane(origin=(0, 0, plate_thickness), x_dir=(1, 0, 0))

        # Curved wall
        with BuildSketch(main_workplane):
            Rectangle(C, C, align=Align.MIN)
            Rectangle(
                C - wall_thickness, C - wall_thickness,
                align=Align.MIN, mode=Mode.SUBTRACT)
            with Locations((C, C)):
                Circle(radius=wall_inner_rad + wall_thickness)
                Circle(radius=wall_inner_rad, mode=Mode.SUBTRACT)
            Rectangle(C, C, align=Align.MIN, mode=Mode.INTERSECT)
        extrude(amount=wall_height)

        # Cylinders
        locations = [
            (cylinder_distance, wall_straight_length/2, total_wall_height),
            (wall_straight_length/2, cylinder_distance, total_wall_height)
        ]
        outer_radii = [Y/2, X/2]
        rotations = [(90, 0, 0), (0, 90, 0)]
        for loc, r, rot in zip(locations, outer_radii, rotations):
            with Locations(loc):
                Cylinder(radius=r, height=D, rotation=rot)
                Cylinder(radius=E/2, height=D, rotation=rot, mode=Mode.SUBTRACT)
        # Cylinder chamfers
        cyl_edges = (
            part.edges()
            .filter_by(GeomType.CIRCLE)
        )
        cyl_edges = [e for e in cyl_edges if e.radius == E/2]
        chamfer(
            cyl_edges,
            length=cylinder_chamfer,
            length2=cylinder_chamfer2
        )
        # Cylinder cut
        cylinder_cut_plane = part.faces().sort_by(Axis.X)[0].offset(-cylinder_cut_offset)
        with BuildSketch(cylinder_cut_plane):
            Circle(X/2)
            Circle(cylinder_cut_radius, mode=Mode.SUBTRACT)
            # Hack to avoid cutting into the wall
            Rectangle(
                100, wall_thickness, 
                align=(Align.MIN, Align.CENTER), mode=Mode.SUBTRACT)
        extrude(amount=-cylinder_cut_height, mode=Mode.SUBTRACT)

        # Offset pockets
        main_faces = part.faces().filter_by(Axis.Z)
        main_faces = ShapeList([
            f for f in main_faces if f.center().Z == plate_thickness
        ]).sort_by(Axis.X)
        pocket1_face = main_faces[0]
        pocket2_face = main_faces[1]
        with BuildSketch(main_workplane):
            make_face(pocket1_face)
            offset(amount=pocket_offset, mode=Mode.REPLACE)
        with BuildSketch(main_workplane):
            make_face(pocket2_face)
            with Locations((A, B)):
                Rectangle(
                    A - wall_straight_length, B - wall_straight_length,
                    align=Align.MAX, mode=Mode.INTERSECT)
            offset(amount=pocket_offset, mode=Mode.REPLACE)
        extrude(amount=pocket_depth, mode=Mode.SUBTRACT)
        pocket_fillet_edges = (
            part.edges(Select.LAST).filter_by(Axis.Z)
        )
        fillet(objects=pocket_fillet_edges, radius=pocket_fillet_radius)

        # Outer fillets
        outer_edges = (
            part.edges()
            .filter_by(Axis.Z)
            .sort_by_distance((A/2, B/2), reverse=True)
        )[:4]
        fillet(outer_edges, radius=outer_fillet_radius)
    return part

results = { name: build(**params) for name, params in inputs.items() }
for name, result in results.items():
    mass = result.part.volume*density
    logging.critical(f"{name} mass: = {mass}")

if "show_object" in locals():
    for name, obj in results.items():
        show_object(obj, name=name)