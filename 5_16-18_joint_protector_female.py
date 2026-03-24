"""Joint Protector for 5/16-18 Cue Joints

Print Setting Recommendations:
- Notes:
    - Use a nightly build of Nanashi fork of OrcaSlicer for Brick Layers (Stagger perimeters) support
        - https://github.com/NanashiTheNameless/OrcaSlicer/releases/tag/Nightly-Rolling
- Quality
    - Layer height: 0.1mm
    - Walls printing order: Odd-Even
    - Odd-Even loop sequence: Outward/Outward
- Strength:
    - Wall loops: 30 (or whatever to fill the part with walls)
    - Stagger perimeters: on
"""

from build123d import *
from bd_warehouse.thread import IsoThread

from vitamins.cue_joint_protector_female import build, get_section_dia, Dome
from vitamins.cue_joint_protector_blank import ALIGN

outer_dia = 21.35
total_length = 40

thread_maj_dia = 5 / 16 * 25.4  # Measures 7.89 mm, assuming 5/16"
thread_pitch = 1 / 18 * 25.4  # Measures 14.08 mm across 10 threads, assuming 18TPI
thread_length = 17
thread_tol = 0.6

_lead_in_length = 4
lead_in_length_tol = 1
lead_in_length = _lead_in_length + lead_in_length_tol

brick_layers_comp = 0.6


thread_maj_dia += brick_layers_comp
_female_thread = IsoThread(
    major_diameter=thread_maj_dia + thread_tol,
    pitch=thread_pitch,
    external=False,
    length=thread_length,
    end_finishes=("fade", "fade"),
)

lead_in_dia = get_section_dia(_female_thread)

lead_in_rest = Cylinder(
    lead_in_dia / 2,
    lead_in_length - lead_in_dia / 2,
    align=ALIGN,
)

lead_in_end = Dome(lead_in_dia / 2)

thread_sections = [
    _female_thread,
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
