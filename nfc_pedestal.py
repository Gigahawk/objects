from build123d import *

from vitamins import dlp_rfid2
from vitamins import adafruit_4090_usb_c_breakout as usb_breakout

topsheet_thickness = 0.4
base_width = 60
base_top_thickness = 3
base_fillet = 10

pcb_xy_tol = 0.2
dlp_offset = 5

with BuildPart() as base_top:
    with BuildSketch() as base_outer_sketch:
        RectangleRounded(base_width, base_width, base_fillet)
    extrude(base_outer_sketch.sketch, amount=topsheet_thickness)
    extrude(base_outer_sketch.sketch, amount=-base_top_thickness)

    bot_face = base_top.faces().filter_by(Axis.Z).sort_by(Axis.Z)[0]

    with BuildSketch(bot_face) as dlp_cutout_sketch:
        with Locations((dlp_offset, 0)):
            # TODO: offset
            Rectangle(dlp_rfid2.pcb_width, dlp_rfid2.pcb_height)
    extrude(dlp_cutout_sketch.sketch, amount=-base_top_thickness, mode=Mode.SUBTRACT)

    with BuildSketch(bot_face) as usb_breakout_sketch:
        # TODO: offset
        with BuildLine():
            add(usb_breakout.outline)
        make_face()
    #extrude(usb_breakout_sketch.sketch, amount=-base_top_thickness, mode=Mode.SUBTRACT)




if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
        )
    except ImportError:
        pass
