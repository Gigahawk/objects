"""Weight spacers for Cuetec cues.

Thread is M18, 2.5mm pitch.

Other details at
https://www.cuetec.com/products/tip-shaft-and-cue-maintenance/acueweight-kit/

Print Settings:
- Layer Height: 0.1mm
- Material: not PLA, PETG preferred
"""

from build123d import *
from bd_warehouse.thread import IsoThread


# thread_length = 27
def build(thread_length):
    # Thread is nominally M18, thread pitch 2.5mm
    thread_maj_dia = 18
    thread_pitch = 2.5

    thread_tol = 0.2

    hex_dia = 10
    hex_tol = 0.2
    hex_relief_dia = 0.4

    _thread = IsoThread(
        major_diameter=thread_maj_dia - thread_tol,
        pitch=thread_pitch,
        length=thread_length,
        external=True,
        end_finishes=["fade", "fade"],
    )

    with BuildPart() as spacer:
        add(_thread)
        Cylinder(
            radius=_thread.min_radius,
            height=thread_length,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        _edges = spacer.edges().filter_by(GeomType.CIRCLE)
        # _fillet = spacer.part.max_fillet(_edges, max_iterations=100)
        # print(f"_fillet: {_fillet}")
        # _fillet = 0.5073343503878373
        # Idk why max_fillet gives this value but its wrong
        chamfer(objects=_edges, length=0.3)
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


results = {f"{tl}mm": build(tl) for tl in [27, 54]}

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
        )
    except ImportError:
        pass
