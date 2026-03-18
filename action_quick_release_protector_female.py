"""Joint Protector for Action Quick Release joint used in the Action ACTBJ09"""
from build123d import *
from bd_warehouse.thread import (
    Thread
)

from vitamins.cue_joint_protector_female import build, get_section_dia, Dome
from vitamins.cue_joint_protector_blank import ALIGN

outer_dia = 21.5
total_length = 42.95

_shoulder_dia = 8
_shoulder_length = 9.15
shoulder_tol = 0.2

thread_maj_dia = (5 / 16) * 25.4
thread_min_dia = 6.9
thread_tip_width = 0.75
thread_root_width = 1.4

# Measures roughly 2.575mm between threads, using closest imperial conversion.
thread_pitch = (3 / 32) * 25.4
thread_length = 8
thread_tol = 0.1

_lead_in_length = 9.6
lead_in_length_tol = 1
_lead_in_dia = 6.45
lead_in_dia_tol = 0.2
lead_in_chamfer_depth = 4

brick_layers_comp = 0.6

shoulder_dia = _shoulder_dia + shoulder_tol
shoulder_length = _shoulder_length + shoulder_tol

lead_in_length = _lead_in_length + lead_in_length_tol
lead_in_dia = _lead_in_dia + lead_in_dia_tol
shoulder_dia += brick_layers_comp
thread_maj_dia += brick_layers_comp
thread_min_dia += brick_layers_comp
lead_in_dia += brick_layers_comp

shoulder = Cylinder(shoulder_dia / 2, shoulder_length, align=ALIGN)

_female_thread = Thread(
    apex_radius=thread_min_dia / 2 + thread_tol,
    apex_width=thread_tip_width,
    root_radius=thread_maj_dia / 2 + thread_tol,
    root_width=thread_root_width,
    pitch=thread_pitch,
    length=thread_length,
    end_finishes=("fade", "fade"),
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
    shoulder,
    _female_thread,
    lead_in_chamfer_cone,
    lead_in_rest,
    lead_in_end,
]


result = build(
    total_length=total_length,
    outer_dia=outer_dia,
    thread_sections=thread_sections
)


if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
        )
    except ImportError:
        pass
