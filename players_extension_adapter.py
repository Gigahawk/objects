"""Extension bumper thread adapter for Players pool cue butt

To this bumper:
https://www.temu.com/goods_snapshot.html?goods_id=601100631369613

Meant to be epoxied into the butt of the cue.
If there is a weight bolt in the butt of the cue you may need to machine down
the diameter of the head so that it can still be removed.
Alternatively Players cues use 1/2"-12TPI threaded weight bolts.
You can use headless (grub) screws instead.

Print Settings:
- Material: not PLA, PETG preferred
- Layer Height: 0.1mm
- Use Arachne perimeter generator
- Maybe disable elephant foot compensation for better adhesion
  unless yours is really dialed in
"""

import logging

import numpy as np
from build123d import *
from bd_warehouse.thread import IsoThread

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

_cavity_dia = 17.5  # tight fit, maybe reduce by 0.05
cavity_dia_tol = 0.0
cavity_dia = _cavity_dia - cavity_dia_tol

thread_len = 16

cut_depth = 0.3
cut_vert_ang = 10
cut_vert_count = 10
cut_horz_height = 2
cut_horz_angle = 30
cut_horz_count = 4
cut_horz_buffer = 1.5


# No idea if the thread is actually ISO, but this reduces the design space
# significantly which is convenient
_inner_thread = IsoThread(
    major_diameter=16.1,
    pitch=11.7 / 8,
    length=thread_len,
    external=False,
    end_finishes=["fade", "fade"],
    interference=0,
)

with BuildPart() as wall:
    outer_rad = cavity_dia / 2
    inner_rad = _inner_thread.major_diameter / 2
    Cylinder(
        radius=outer_rad,
        height=thread_len,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    Cylinder(
        radius=inner_rad,
        height=thread_len,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
        mode=Mode.SUBTRACT,
    )
    with BuildSketch() as vert_cutout_sketch:
        with BuildLine() as vert_cutout_lines:
            path = CenterArc(
                center=(0, 0),
                radius=outer_rad,
                start_angle=0,
                arc_size=cut_vert_ang,
            )
            profile = PolarLine(
                start=(outer_rad, 0),
                length=cut_depth,
                direction=(-1, -0),
            )
        _cut_outline = sweep(sections=profile, path=path, mode=Mode.PRIVATE)
        with PolarLocations(radius=0, count=cut_vert_count):
            add(_cut_outline)
    extrude(until=Until.LAST, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XZ) as horz_cutout_sketch:
        grid_length = thread_len - 2 * cut_horz_buffer - cut_horz_height
        grid_spacing = grid_length / (cut_horz_count - 1)
        with GridLocations(
            x_count=1,
            x_spacing=0,
            y_count=cut_horz_count,
            y_spacing=grid_spacing,
            align=None,
        ):
            with Locations((outer_rad, cut_horz_height / 2 + cut_horz_buffer)):
                Trapezoid(
                    width=cut_horz_height,
                    height=cut_depth,
                    left_side_angle=cut_horz_angle,
                    rotation=90,
                    align=(Align.CENTER, Align.MIN),
                )
    revolve(mode=Mode.SUBTRACT)


with BuildPart() as part:
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
