"""Thread adapter for pool cue extension bumper
"""

from build123d import *
from bd_warehouse.thread import IsoThread

thread_len = 16

_inner_thread = IsoThread(
    major_diameter=15.25,
    pitch=11.7/8,
    length=thread_len,
    external=False,
    end_finishes=["fade","fade"]
)

_outer_thread = IsoThread(
    major_diameter=17.95,
    pitch=9.75/4,
    length=thread_len,
    external=True,
    end_finishes=["fade","fade"]
)

# Seems like the IsoThread objects have a little extra thickness added to them
# that causes us issues, get rid of it
with BuildPart() as inner_thread:
    add(_inner_thread)
    Cylinder(
        radius=_inner_thread.major_diameter/2, height=thread_len,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
        mode=Mode.INTERSECT
    )
with BuildPart() as outer_thread:
    add(_outer_thread)
    Cylinder(
        radius=_outer_thread.min_radius, height=thread_len,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
        mode=Mode.SUBTRACT
    )
with BuildPart() as wall:
    Cylinder(
        radius=_outer_thread.min_radius, height=thread_len,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    Cylinder(
        radius=_inner_thread.major_diameter/2, height=thread_len,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
        mode=Mode.SUBTRACT
    )

with BuildPart() as part:
    add(outer_thread)
    add(inner_thread)
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

