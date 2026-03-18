from math import tan, radians

from build123d import *
from bd_warehouse.thread import (
    AcmeThread,
    IsoThread,
    MetricTrapezoidalThread,
    PlasticBottleThread,
    Thread,
    TrapezoidalThread,
)

from vitamins.cue_joint_protector_blank import CueJointProtectorBlank, ALIGN

THREAD_CLASSES = (
    Thread,
    IsoThread,
    AcmeThread,
    MetricTrapezoidalThread,
    TrapezoidalThread,
    PlasticBottleThread,
)

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

def build(
    thread_sections: list[BasePartObject] = [],
    **kwargs,
) -> Compound:
    with BuildPart() as _female:
        CueJointProtectorBlank(**kwargs)

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
    return female


default = build(
    total_length = 42.95,
    outer_dia = 21.5,
    thread_sections = [
        Cylinder(3, 10, align=ALIGN)
    ]
)

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(reset_camera=Camera.KEEP, render_joints=True)
    except ImportError:
        pass
