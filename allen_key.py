"""Allen/hex keys"""

from build123d import *

_flat_to_flat_dist = 6
tol = 0.1
flat_to_flat_dist = _flat_to_flat_dist - tol
long_length = 210
short_length = 60
bend_rad = 10

with BuildPart() as allen_key:
    with BuildLine() as path:
        FilletPolyline(
            [
                (0, 0, 0),
                (0, 0, long_length),
                (short_length, 0, long_length),
            ],
            radius=bend_rad,
        )
    with BuildSketch() as profile:
        RegularPolygon(radius=flat_to_flat_dist / 2, side_count=6, major_radius=False)
    sweep(sections=profile.sketch, path=path.line)


result = allen_key.part


if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(reset_camera=Camera.KEEP, render_joints=True)
    except ImportError:
        pass
