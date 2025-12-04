from build123d import *
from pathlib import Path

out = import_step(Path(__file__).parent.parent / "res/4090_USB_C_Breakout.step")
out.color = Color("blue")

# HACK: The first two faces happen to be the two PCB faces.
# We can't just sort by Z first because the bottoms of the resistors
# actually sit a little below the top surface
pcb_faces = out.faces().filter_by(Axis.Z)[0:2].sort_by(Axis.Z)
bot_face, top_face = pcb_faces

nom_pcb_thickness = bot_face.center().Z - top_face.center().Z

outline = bot_face.outer_wire()

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
        )
    except ImportError:
        pass
