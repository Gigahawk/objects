"""Dummy SD card to use as a dust cover for empty slots"""
from build123d import *

outer_thickness = 1.4
outer_width = 24
outer_length = 32
outer_chamfer = 4
outer_chamfer_fillet = 0.5
outer_fillet = 1
switch_offset = 7.8
switch_length = 6.7
switch_fillet = 0.3
notch_offset = 10
notch_length = 1.5
inner_width = 22.5
inner_fillet = 0.5
inner_thickness = 0.6  # best guess
pin_cutout_depth = 7.95
pin_cutout_width = 21  # best guess
pin_cutout_offset = 0.6  # best guess
lip_width = (outer_width - inner_width)/2

with BuildPart() as base:
    with BuildSketch(Plane.XY) as outer_sketch:
        Rectangle(outer_width, outer_length, align=(Align.MIN, Align.MAX))
        chamfer_corner = outer_sketch.vertices().sort_by(Axis.X).sort_by(Axis.Y, reverse=True)[0]
        other_corners = [c for c in outer_sketch.vertices() if c != chamfer_corner]
        # Cutout for lock switch
        with Locations((outer_width, -switch_offset)):
            Rectangle(lip_width, switch_length, align=Align.MAX, mode=Mode.SUBTRACT)
            switch_corners = outer_sketch.vertices(Select.LAST).sort_by(Axis.X)[2:]
        # Cutout for notch
        with Locations((0, -notch_offset)):
            Rectangle(lip_width, notch_length, align=(Align.MIN, Align.MAX), mode=Mode.SUBTRACT)
        chamfer(chamfer_corner, length=outer_chamfer)
        chamfer_fillet_corners = outer_sketch.vertices(Select.LAST)
        fillet(chamfer_fillet_corners, radius=outer_chamfer_fillet)
        fillet(switch_corners, radius=switch_fillet)
        fillet(other_corners, radius=outer_fillet)
    extrude(amount=outer_thickness)
    outer_top_plane = Plane((0, 0, outer_thickness))
    with BuildSketch(outer_top_plane) as inner_sketch:
        with Locations((lip_width, 0)):
            Rectangle(inner_width, outer_length, align=(Align.MIN, Align.MAX))
            with Locations((pin_cutout_offset, 0)):
                Rectangle(
                    pin_cutout_width, pin_cutout_depth, align=(Align.MIN, Align.MAX),
                    mode=Mode.SUBTRACT)
        inner_chamfer_corners = inner_sketch.vertices().sort_by(Axis.Y)[:2]
        fillet(inner_chamfer_corners, radius=inner_fillet)
        add(outer_sketch, mode=Mode.INTERSECT)
    extrude(amount=inner_thickness)


results = {
    "base": base.part,
}

if __name__ == "__main__":
    if "show_object" in locals():
        show_object(results["lian_li_power_button"])

    try:
        from ocp_vscode import *
        show_all()
    except:
        pass
