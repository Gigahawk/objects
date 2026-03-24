"""Joint Protector for 5/16-18 cue joints

BOM:
- 1x M2.5 square nut
- 1x M2.5 40mm long socket head screw

Print Setting Recommendations:
- Notes:
    - Use a nightly build of Nanashi fork of OrcaSlicer for Brick Layers (stagger perimeters) support
        - https://github.com/NanashiTheNameless/OrcaSlicer/releases/tag/Nightly-Rolling
    - Insert a print pause on the top layer of the square nut to allow for mid-print insertion.
        - IMPORTANT: the layer slider thing is often broken when stagger perimeters is enabled.
          You may have to manually edit the G-code to get the pause to actually happen at the right
          spot.
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

from vitamins.cue_joint_protector_male import build

outer_dia = 21.15
total_length = 45

thread_maj_dia = 5 / 16 * 25.4  # Measures 7.89 mm, assuming 5/16"
thread_pitch = 1 / 18 * 25.4  # Measures 14.08 mm across 10 threads, assuming 18TPI
thread_length = 10
thread_tol = 0.1


_male_thread = IsoThread(
    major_diameter=thread_maj_dia - thread_tol,
    pitch=thread_pitch,
    external=True,
    length=thread_length,
    end_finishes=("fade", "fade"),
)
thread_min_dia = _male_thread.min_radius * 2

thread_sections = [_male_thread]

result = build(
    stem_dia=thread_min_dia,
    stem_extra_len=0,
    total_length=total_length,
    outer_dia=outer_dia,
    thread_sections=thread_sections,
)


if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
        )
    except ImportError:
        pass
