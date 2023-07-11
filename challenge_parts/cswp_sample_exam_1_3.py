"""Part from the Q1-Q3 of SOLIDWORKS CSWP Sample Exam

https://www.solidworks.com/certifications/mechanical-design-cswp-mechanical-design
"""

import logging

from build123d import *

density = 0.0077  # g/mm^3

inputs = {
    "q1": {
        "A": 213,
        "B": 200,
        "C": 170,
        "D": 130,
        "E": 41,
        "Fr": 30/2,
        "Fd": 10,
        "FR": 15/2,
    },
    "q2": {
        "A": 225,
        "B": 210,
        "C": 176,
        "D": 137,
        "E": 39,
        "Fr": 30/2,
        "Fd": 10,
        "FR": 15/2,
    },
    "q3": {
        "A": 209,
        "B": 218,
        "C": 169,
        "D": 125,
        "E": 41,
        "Fr": 30/2,
        "Fd": 10,
        "FR": 15/2,
    },
}

def build(A, B, C, D, E, Fr, Fd, FR):
    plate_thickness = 25
    wall_straight_length = 80
    wall_inner_rad = C - wall_straight_length
    wall_thickness = 15
    wall_height = 95 - plate_thickness
    total_wall_height = wall_height + plate_thickness
    cylinder_distance = C - wall_thickness/2
    cylinder_chamfer = 2
    counterbore_radius = Fr
    counterbore_depth = Fd
    counterbore_through_radius = FR
    counterbore_platform_width = 60
    counterbore_platform_height = 35 - plate_thickness
    counterbore_fillet_radius = 15
    outer_fillet_radius = 10
    pocket_offset = -9
    pocket_depth = 5 - plate_thickness
    pocket_fillet_radius = 10

    X = A/3
    Y = B/3 + 10

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

        # Counterbore hole platform
        with BuildSketch(main_workplane):
            Rectangle(counterbore_platform_width, counterbore_platform_width, 
                    align=Align.MIN)
        extrude(amount=counterbore_platform_height)
        with Locations(part.faces(Select.LAST).sort_by(Axis.Z)[-1]):
            CounterBoreHole(
                radius=counterbore_through_radius,
                counter_bore_radius=counterbore_radius,
                counter_bore_depth=counterbore_depth
            )

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
            length=cylinder_chamfer
        )

        # Outer fillets
        outer_edges = (
            part.edges()
            .filter_by(Axis.Z)
            .sort_by_distance((A/2, B/2), reverse=True)
        )[:4]
        fillet(outer_edges, radius=outer_fillet_radius)

        # Counterbore hole fillet
        counterbore_edge = (
            part.edges()
            .filter_by(Axis.Z)
            .sort_by_distance((counterbore_platform_width, counterbore_platform_width))
        )[0]
        fillet(counterbore_edge, radius=counterbore_fillet_radius)

        # Offset pocket
        main_faces = part.faces().filter_by(Axis.Z)
        main_faces = ShapeList([
            f for f in main_faces if f.center().Z == plate_thickness
        ])
        # 0 index happens to be the counterbore hole in this case.
        # A more robust way may be to filter faces by size to prevent the counterbore
        # from being a part of main_faces
        pocket_face = main_faces.sort_by(Axis.X)[1]
        with BuildSketch(main_workplane):
            make_face(pocket_face)
            offset(amount=pocket_offset, mode=Mode.REPLACE)
        extrude(amount=pocket_depth, mode=Mode.SUBTRACT)
        # Pocket fillets
        pocket_fillet_edges = (
            part.edges(Select.LAST).filter_by(Axis.Z)
        )
        fillet(objects=pocket_fillet_edges, radius=pocket_fillet_radius)
    return part

results = { name: build(**params).part for name, params in inputs.items() }
for name, rslt in results.items():
    mass = rslt.volume*density
    logging.critical(f"{name} mass: = {mass}")

if "show_object" in locals():
    for name, obj in results.items():
        show_object(obj, name=name)