"""Stroke trainer for billiards"""

from build123d import *


def build_trainer(
    ball_dia: float,
    base_dia: float,
    base_thickness: float,
    base_fillet: float,
    base_chamfer: float,
    hole_dia: float,
    hole_taper: float,
    hole_fillet: float,
    layer_thickness: float = 0.2,
    magnet_dia: float = 6.0,
    magnet_thickness: float = 3.0,
    magnet_tol: float = 0.1,
    magnet_count: int = 6,
):
    """Build the object

    Args:
        ball_dia: the outer diameter of the billiard ball
        base_dia: outer diameter of the base
        base_thickness: thickness of the base
        base_fillet: fillet radius between ball and base
        base_chamfer: chamfer width of base edge
        hole_dia: diameter of the hole AT THE BALL CENTER
        hole_taper: taper angle of hole
        hole_fillet: fillet radius between ball and hole
        layer_thickness: thickness of first layer for magnets
    """
    with BuildPart() as ball:
        # Cut tool has to be separate for some reason, doesn't
        # work if we subtract directly
        with BuildSketch(Plane.XZ, mode=Mode.PRIVATE) as _tool:
            Rectangle(
                ball_dia,
                ball_dia / 1.9,
                align=(Align.CENTER, Align.MAX),
                # mode=Mode.SUBTRACT
            )
            with BuildLine():
                PolarLine((0, hole_dia / 1.9), ball_dia / 1.9, angle=hole_taper)
                PolarLine((0, hole_dia / 1.9), ball_dia / 1.9, angle=180 + hole_taper)
                Line((-ball_dia / 1.9, 0), (ball_dia / 1.9, 0))
            make_hull()
        with BuildSketch(Plane.XZ):
            Circle(ball_dia / 2)
            add(_tool, mode=Mode.SUBTRACT)
        revolve(axis=Axis.X)
        # There will always be 3 circular edges, two hole edges, and one
        # "fake" edge along the surface of the ball caused by OCP.
        # The hole edges can never be larger than the fake edge
        hole_edges = ball.edges().filter_by(GeomType.CIRCLE).sort_by(SortBy.RADIUS)[0:2]
        fillet(hole_edges, hole_fillet)

        with Locations((0, 0, -ball_dia / 2)):
            Cylinder(
                base_dia / 2,
                base_thickness,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
        top_surface_coord = -ball_dia / 2 + base_thickness
        fillet_edge, chamfer_edge = (
            ball.edges(Select.LAST)
            .filter_by_position(Axis.Z, top_surface_coord, top_surface_coord)
            .sort_by(SortBy.RADIUS)
        )
        fillet(fillet_edge, base_fillet)
        chamfer(chamfer_edge, base_chamfer)

        magnet_hole_rad = (ball_dia - hole_dia) / 2

        with BuildPart(mode=Mode.SUBTRACT):
            with Locations(Plane.ZY):
                with PolarLocations(magnet_hole_rad, count=magnet_count):
                    Cylinder(
                        radius=(magnet_dia + magnet_tol) / 2,
                        height=(magnet_thickness + layer_thickness + magnet_tol) * 2,
                    )
                    Cylinder(
                        radius=ball_dia / 2,
                        height=layer_thickness * 2,
                        mode=Mode.SUBTRACT,
                    )
        split(ball.part, Plane.YZ, keep=Keep.BOTH)
    return ball


results = {
    "american": build_trainer(57.15, 55, 8, 3, 3, 17, 1, 3).part,
}

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show(results["american"])
        # show_all(
        #    reset_camera=Camera.KEEP,
        # )
    except ImportError:
        pass
