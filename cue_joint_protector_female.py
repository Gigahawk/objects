"""Joint Protector for Action Quick Release joint used in the Action ACTBJ09"""

from build123d import *
from bd_warehouse.thread import (
    AcmeThread,
    IsoThread,
    MetricTrapezoidalThread,
    PlasticBottleThread,
    Thread,
    TrapezoidalThread,
)

from math import tan, radians

THREAD_CLASSES = (
    Thread,
    IsoThread,
    AcmeThread,
    MetricTrapezoidalThread,
    TrapezoidalThread,
    PlasticBottleThread,
)


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
    raise NotImplementedError(
        f"get_section_height not implemented for type {type(section)}"
    )


ALIGN = (Align.CENTER, Align.CENTER, Align.MIN)

num_faces = 6

outer_dia = 21.5

total_length = 42.95

protection_ring_thickness = 1.25
protection_ring_height = 6
protection_ring_upper_chamfer_len = 2
# HACK: To compensate for loft cut
protection_ring_extra = 0.2

_shoulder_dia = 8
_shoulder_length = 9.15
shoulder_tol = 0.2
shoulder_dia = _shoulder_dia + shoulder_tol
shoulder_length = _shoulder_length + shoulder_tol

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
lead_in_length = _lead_in_length + lead_in_length_tol
_lead_in_dia = 6.45
lead_in_dia_tol = 0.2
lead_in_dia = _lead_in_dia + lead_in_dia_tol
lead_in_chamfer_depth = 4

brick_layers_comp = 0.6
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
    lead_in_length - lead_in_chamfer_depth,
    align=ALIGN,
)

# TODO: half sphere domed top

thread_sections = [
    shoulder,
    _female_thread,
    lead_in_chamfer_cone,
    lead_in_rest,
]


with BuildPart() as female:
    with BuildSketch():
        Circle(outer_dia / 2)
    extrude(amount=total_length)
    section_height = 0
    for section in thread_sections:
        height = get_section_height(section)
        if isinstance(section, THREAD_CLASSES):
            thread_outer_dia = get_section_dia(section)
            with Locations((0, 0, section_height)):
                Cylinder(thread_outer_dia / 2, height, mode=Mode.SUBTRACT, align=ALIGN)
                add(section)
        else:
            with Locations((0, 0, section_height)):
                add(
                    section,
                    mode=Mode.SUBTRACT,
                )
        section_height += height

    top_face = female.faces().sort_by(Axis.Z)[-1]
    bot_face = female.faces().sort_by(Axis.Z)[0]
    with BuildSketch(top_face) as loft_top:
        RegularPolygon(
            side_count=num_faces,
            radius=outer_dia / 2,
            major_radius=True,
        )
    with BuildSketch(bot_face) as loft_bot:
        RegularPolygon(
            side_count=num_faces,
            radius=outer_dia / 2,
            major_radius=False,
        )
    loft(sections=[loft_top.sketch, loft_bot.sketch], mode=Mode.INTERSECT)


results = {
    "female": female.part,
}

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
        )
    except ImportError:
        pass
