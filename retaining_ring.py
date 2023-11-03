"""Retaining rings/collars for holding in cylindrical parts
"""
from build123d import *

def build(inner_dia, planar_thickness, radial_thickness, gap_angle=45,
          tab_length=None, fillet_radius=None):
    if tab_length is None:
        tab_length = radial_thickness*2
    if fillet_radius is None:
        fillet_radius = radial_thickness/3
    half_gap = gap_angle/2
    with BuildPart() as part:
        with BuildSketch():
            with BuildLine():
               c1 = CenterArc((0, 0), inner_dia/2, half_gap, 180 - half_gap)
               PolarLine(c1@0, tab_length, half_gap)
               offset(amount=radial_thickness, side=Side.RIGHT)
            make_face()
        p = extrude(amount=planar_thickness)
        mirror(p)
        fillet(
            part.edges().filter_by(Axis.Z),
            fillet_radius)
    return part



results = {
    "lian_li_power_button": build(20, 2, 1.5).part,
}

if __name__ == "__main__":
    if "show_object" in locals():
        show_object(results["lian_li_power_button"])

    try:
        from ocp_vscode import *
        show(results["lian_li_power_button"])
    except:
        pass