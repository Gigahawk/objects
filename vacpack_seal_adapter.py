"""Battery retention bracket for the Flyby Accugun Pro"""

from build123d import *

seal_inner_dia = 36.5
seal_outer_dia = 41.5
seal_height = 9
wall_thickness = (seal_outer_dia - seal_inner_dia)/2

vac_dia = 16.5
inner_chamfer1 = 2
inner_chamfer2 = 1
outer_chamfer1 = 2
outer_chamfer2 = 1

with BuildPart() as adapter:
    with BuildSketch():
        Circle(seal_outer_dia/2)
        Circle(vac_dia/2, mode=Mode.SUBTRACT)
    extrude(amount=wall_thickness)

    top_face = adapter.faces().sort_by(Axis.Z, reverse=True)[0]

    with BuildSketch(top_face):
        Circle(seal_outer_dia/2)
        Circle(seal_inner_dia/2, mode=Mode.SUBTRACT)
    extrude(amount=seal_height)

    outer_corner, _, _, inner_corner = adapter.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z)[0:4]
    chamfer(outer_corner, length=outer_chamfer1, length2=outer_chamfer2)
    #chamfer(inner_corner, length=inner_chamfer1, length2=inner_chamfer2)


result = adapter.part

if __name__ == "__main__":
    if "show_object" in locals():
        show_object(adapter)

    try:
        from ocp_vscode import *
        show_all()
    except ImportError:
        pass

