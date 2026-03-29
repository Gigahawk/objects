"""Joint Protector for 3/8-10 cue joints"""

from build123d import *
from bd_warehouse.thread import IsoThread

from vitamins.cue_joint_protector_female import build, get_section_dia, Dome, ALIGN


outer_dia = 20.8
total_length = 30

thread_maj_dia = (3 / 8) * 25.4

thread_pitch = (1 / 10) * 25.4
thread_length = 12
thread_tol = 0.6

_lead_in_length = 11
lead_in_length_tol = 1
lead_in_length = _lead_in_length + lead_in_length_tol
_lead_in_dia = 6.4
lead_in_dia_tol = 0.2
lead_in_dia = _lead_in_dia + lead_in_dia_tol
lead_in_chamfer_depth = 4

# OrcaSlicer fork provides a brick layers option with overextrusion for better strength.
# This seems to screw up the internal dimensions.
# Compensating for 1.1 flow ratio on even loops
# brick_layers_comp = 0.4  # seems to be fine straight off the build plate but a little too tight after washing?
brick_layers_comp = 0.6
thread_maj_dia += brick_layers_comp
lead_in_dia += brick_layers_comp


_female_thread = IsoThread(
    major_diameter=thread_maj_dia + thread_tol,
    pitch=thread_pitch,
    external=False,
    length=thread_length,
    end_finishes=("fade", "fade"),
    interference=2,  # HACK: fix broken overlap
)

lead_in_chamfer_cone = Cone(
    bottom_radius=get_section_dia(_female_thread) / 2,
    top_radius=lead_in_dia / 2,
    height=lead_in_chamfer_depth,
    align=ALIGN,
)

lead_in_rest = Cylinder(
    lead_in_dia / 2,
    lead_in_length - lead_in_chamfer_depth - lead_in_dia / 2,
    align=ALIGN,
)

lead_in_end = Dome(lead_in_dia / 2)

thread_sections = [
    _female_thread,
    lead_in_chamfer_cone,
    lead_in_rest,
    lead_in_end,
]

result = build(
    total_length=total_length, outer_dia=outer_dia, thread_sections=thread_sections
)

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
        )
    except ImportError:
        pass
