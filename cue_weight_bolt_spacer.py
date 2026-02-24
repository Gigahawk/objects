"""Weight spacers for pool cues.


Print Settings:
- Layer Height: 0.1mm
- Material: not PLA, PETG preferred
"""

from build123d import *
from bd_warehouse.thread import IsoThread


# thread_length = 27
def build(thread_length, thread_maj_dia, thread_pitch, hex_dia, end_chamfer=0.1):
    thread_tol = 0.2

    hex_tol = 0.2
    hex_relief_dia = 0.4

    _thread = IsoThread(
        major_diameter=thread_maj_dia - thread_tol,
        pitch=thread_pitch,
        length=thread_length,
        external=True,
        end_finishes=["fade", "fade"],
    )

    assert hex_dia < _thread.min_radius * 2

    with BuildPart() as spacer:
        add(_thread)
        Cylinder(
            radius=_thread.min_radius,
            height=thread_length,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        _edges = spacer.edges().filter_by(GeomType.CIRCLE)
        chamfer(objects=_edges, length=end_chamfer)
        with BuildSketch() as hex_sketch:
            RegularPolygon(
                radius=(hex_dia + hex_tol) / 2,
                side_count=6,
                major_radius=False,
            )
            points = hex_sketch.vertices()
            with Locations(points):
                Circle(radius=hex_relief_dia / 2)
        # Extrude through the whole length, avoid a solid section since the join is
        # a stress concentration. Also if the part breaks there will still be a hole
        # to remove the pieces
        extrude(amount=thread_length, mode=Mode.SUBTRACT)
    return spacer.part


# Thread is nominally M18, thread pitch 2.5mm

# Other details at
# https://www.cuetec.com/products/tip-shaft-and-cue-maintenance/acueweight-kit/
cuetec_results = {
    f"cuetec-{tl}mm": build(
        thread_length=tl,
        thread_maj_dia=18,
        thread_pitch=2.5,
        hex_dia=10,
        end_chamfer=0.3,
    )
    for tl in [27, 54]
}

# Thread is nominally 1/2", 12TPI
player_results = {
    f"player-{tl}mm": build(
        thread_length=tl,
        thread_maj_dia=0.5 * IN,
        thread_pitch=IN / 12,
        hex_dia=6,
        end_chamfer=0.01,
    )
    for tl in [15, 25]
}

results = player_results | cuetec_results

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
        )
    except ImportError:
        pass
