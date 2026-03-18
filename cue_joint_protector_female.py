"""Joint protector for various pool cues"""

from build123d import *
from bd_warehouse.thread import (
    AcmeThread,
    IsoThread,
    MetricTrapezoidalThread,
    PlasticBottleThread,
    Thread,
    TrapezoidalThread,
)

from vitamins.cue_joint_protector_blank import CueJointProtectorBlank

from math import tan, radians

THREAD_CLASSES = (
    Thread,
    IsoThread,
    AcmeThread,
    MetricTrapezoidalThread,
    TrapezoidalThread,
    PlasticBottleThread,
)

ALIGN = (Align.CENTER, Align.CENTER, Align.MIN)


class Dome(Sphere):
    def __init__(self, *args, align=ALIGN, **kwargs):
        super().__init__(*args, arc_size1=0, align=align, **kwargs)


def get_section_dia(section) -> float:
    if isinstance(section, Thread):
        # Only for female thread
        return section.root_radius * 2
    raise NotImplementedError(
        f"get_section_dia not implemented for type {type(section)}"
    )


def get_section_height(section) -> float:
    if isinstance(section, Thread):
        return section.length
    if isinstance(section, Cylinder):
        return section.cylinder_height
    if isinstance(section, Cone):
        return section.cone_height
    try:
        bb = section.bounding_box()
        return bb.size.Z
    except AttributeError:
        raise NotImplementedError(
            f"get_section_height not implemented for type {type(section)}"
        )


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

top_loft_chamfer_inset = 1.5
top_loft_chamfer_angle = 60
top_secondary_chamfer_len = 1

notch_start = 4
notch_height = 1
notch_depth = 0.8
notch_count = 3
notch_offset = 2.5

top_chamfer_loft_top_dia = outer_dia - 2 * top_loft_chamfer_inset
top_chamfer_loft_bot_dia = top_chamfer_loft_top_dia + 2 * (
    total_length / tan(radians(top_loft_chamfer_angle))
)

shoulder_dia = _shoulder_dia + shoulder_tol
shoulder_length = _shoulder_length + shoulder_tol

lead_in_length = _lead_in_length + lead_in_length_tol
lead_in_dia = _lead_in_dia + lead_in_dia_tol
shoulder_dia += brick_layers_comp
thread_maj_dia += brick_layers_comp
thread_min_dia += brick_layers_comp
lead_in_dia += brick_layers_comp
protection_ring_dia = outer_dia + protection_ring_thickness * 2

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

with BuildPart() as _female:
    CueJointProtectorBlank(
        total_length=total_length,
        outer_dia = outer_dia,
    )

    section_height = 0
    section_height_map = {}
    for section in thread_sections:
        section_height_map[section] = section_height
        height = get_section_height(section)
        if isinstance(section, THREAD_CLASSES):
            thread_outer_dia = get_section_dia(section)
            with Locations((0, 0, section_height)):
                Cylinder(thread_outer_dia / 2, height, mode=Mode.SUBTRACT, align=ALIGN)
                # add(section)
        else:
            with Locations((0, 0, section_height)):
                add(
                    section,
                    mode=Mode.SUBTRACT,
                )
        section_height += height

female = Compound(
    [_female.part]
    + [
        s.moved(Location((0, 0, section_height_map[s])))
        for s in thread_sections
        if isinstance(s, THREAD_CLASSES)
    ]
)

results = {
    "female": female,
}

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
        )
    except ImportError:
        pass
