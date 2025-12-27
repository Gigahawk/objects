"""Thread adapter for pool cue extension bumper

Meant to adapt the butt of this cue:
https://www.temu.com/goods.html?_bg_fs=1&goods_id=601100587774219
> It seems like the butt of the cue is using a standard M18x2.5 Cuetec style
thread.

To this bumper:
https://www.temu.com/goods_snapshot.html?goods_id=601100631369613
Note that the picture shows a coarse threaded bumper that might actually fit,
but what I actually recieved had a much finer thread than shown in the picture

Print Settings:
- Material: not PLA, PETG preferred
- Layer Height: 0.1mm
- Use Arachne perimeter generator
- Probably disable elephant foot compensation unless yours is really dialed in
"""

import logging

from build123d import *
from bd_warehouse.thread import IsoThread

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

thread_len = 16
# PrusaSlicer seems to not be able to extrude any thinner than this
min_wall_thickness = 0.15
base_thickness = 0.2
# Create built in brim to improve printability
base_dia = 19.3


# No idea if the thread is actually ISO, but this reduces the design space
# significantly which is convenient
_inner_thread = IsoThread(
    major_diameter=16,
    pitch=11.7 / 8,
    length=thread_len,
    external=False,
    end_finishes=["fade", "fade"],
    interference=0,
)

_outer_thread = IsoThread(
    major_diameter=18,
    pitch=2.5,
    length=thread_len,
    external=True,
    end_finishes=["fade", "fade"],
    interference=0,
)

with BuildPart() as wall:
    outer_rad = _outer_thread.min_radius
    inner_rad = _inner_thread.major_diameter / 2
    wall_thickness = outer_rad - inner_rad
    if wall_thickness < min_wall_thickness:
        logger.warning(
            f"Nominal wall thickness is {wall_thickness}, expanding to {min_wall_thickness}"
        )
        # Inner thread is smaller and probably more sensitive to tolerance deviations,
        # Expand into outer thread
        outer_rad = inner_rad + min_wall_thickness
    Cylinder(
        radius=outer_rad,
        height=thread_len,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    Cylinder(
        radius=base_dia / 2,
        height=base_thickness,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    Cylinder(
        radius=inner_rad,
        height=thread_len,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
        mode=Mode.SUBTRACT,
    )

# Ensure outer thread is trimmed to not intersect with wall
with BuildPart() as outer_thread:
    add(_outer_thread)
    Cylinder(
        radius=outer_rad,
        height=thread_len,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
        mode=Mode.SUBTRACT,
    )

with BuildPart() as part:
    add(outer_thread)
    add(_inner_thread)
    add(wall)

result = part.part

if __name__ == "__main__":
    if "show_object" in locals():
        show_object(result)

    try:
        from ocp_vscode import *

        show_all()
    except ImportError:
        pass
