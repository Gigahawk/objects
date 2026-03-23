"""Joint Protector for Action Quick Release joint used in the Action ACTBJ09"""

from build123d import *
from bd_warehouse.thread import Thread

from vitamins.cue_joint_protector_male import build


outer_dia = 21.5
total_length = 48.45

_shoulder_length = 9.15
shoulder_tol = 0.1
shoulder_length = _shoulder_length - shoulder_tol

thread_maj_dia = (5 / 16) * 25.4
thread_min_dia = 6.9
thread_tip_width = 0.75
thread_root_width = 1.4

# Measures roughly 2.575mm between threads, using closest imperial conversion.
thread_pitch = (3 / 32) * 25.4
thread_length = 8
thread_tol = 0.1


_male_thread = Thread(
    apex_radius=thread_maj_dia / 2 - thread_tol,
    apex_width=thread_tip_width,
    root_radius=thread_min_dia / 2 - thread_tol,
    root_width=thread_root_width,
    pitch=thread_pitch,
    length=thread_length,
    end_finishes=("fade", "fade"),
)
thread_min_dia = _male_thread.root_radius * 2
thread_sections = [_male_thread]

result = build(
    stem_dia=thread_min_dia,
    stem_extra_len=shoulder_length,
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
