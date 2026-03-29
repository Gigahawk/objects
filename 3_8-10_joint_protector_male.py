"""Joint Protector for 3/8-10 cue joints"""

from build123d import *
from bd_warehouse.thread import IsoThread

from vitamins.cue_joint_protector_male import build

outer_dia = 20.8
total_length = 34

thread_maj_dia = (3 / 8) * 25.4

thread_pitch = (1 / 10) * 25.4
thread_length = 8
thread_tol = 0.1
thread_inset = 4


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
