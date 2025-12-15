"""Tools to hold sandpaper for sanding mating surface of this cue extension:
https://www.temu.com/goods_snapshot.html?goods_id=601100631369613
"""

from build123d import *

main_rad = 31.5 / 2
extra_rad = 10

hole_rad = 10 / 2

tool_height = 15
chamfer_tool_height = 20
tool_rad = main_rad + extra_rad


with BuildPart() as flat:
    Cylinder(radius=tool_rad, height=tool_height)
    Cylinder(radius=hole_rad, height=tool_height, mode=Mode.SUBTRACT)


with BuildPart() as chamferred:
    with BuildSketch(Plane.XZ) as side_profile:
        with BuildLine() as side_profile_ln:
            l1 = Polyline(
                [
                    (tool_rad, 0),
                    (tool_rad, chamfer_tool_height),
                    (tool_rad - chamfer_tool_height, 0),
                ],
                close=True,
            )
        make_face()
    revolve(axis=Axis.Z)


results = {
    "flat": flat.part,
    "chamferred": chamferred.part,
}

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all()
    except ImportError:
        pass
