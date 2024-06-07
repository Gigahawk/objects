"""PCIe bracket mount for a 128x32 SSD1306 display module
"""

import logging
from build123d import *

from pcie_bracket import (
    bracket, main_length, thickness, full_height, main_height, support_gap
)

pcb_width = 38.2
pcb_height = 12.1
pcb_vertical_offset = 0
module_thickness = 3.2
tolerance = 0.25
guide_thickness = module_thickness
guide_support_hole_width = 7
guide_support_chamfer_depth = 2
tab_extra_support_width = 10
tab_gap = 0.2
tab_thickness = 1.2
tab_length = 12
tab_chamfer_depth = 6
cutout_width = 23.8
cutout_height = 8
cutout_taper = 45
cutout_chamfer = 0.8
cutout_horizontal_offset = -0.75
cutout_vertical_offset = 0.75
window_support_gap = 2
clip_offset = 3
clip_width = 10
clip_thickness = 2
clip_overhang = 0.4
clip_chamfer_angle = 30

_cutout_vertical_offset = cutout_vertical_offset + pcb_vertical_offset
_pcb_width = pcb_width + tolerance
_pcb_height = pcb_height + tolerance
tab_support_width = tab_extra_support_width + guide_thickness
guide_outer_width = pcb_width + 2*guide_thickness
nominal_guide_height = (main_height - pcb_height)/2
bottom_guide_height = nominal_guide_height + pcb_vertical_offset
top_guide_height = nominal_guide_height - pcb_vertical_offset


with BuildPart() as mount:
    add(bracket)
    mount_face = (
        mount.faces().sort_by(Axis.Y)
        .sort_by_distance(
            (main_length/2, -thickness, full_height/2))
    )[0]
    with BuildSketch(mount_face) as mount_sketch:
        with Locations((0, mount_face.center().Z)):
            Rectangle(
                guide_outer_width, main_height,
                align=(Align.CENTER, Align.MAX))
            with Locations((guide_outer_width/2, 0)):
                Rectangle(
                    tab_extra_support_width, main_height,
                    align=(Align.MIN, Align.MAX)
                )
        with Locations((0, mount_face.center().Z - main_height/2 + pcb_vertical_offset)):
            Rectangle(
                _pcb_width, _pcb_height,
                mode=Mode.SUBTRACT)
    extrude(amount=guide_thickness)
    guide_face = mount.faces().sort_by(Axis.Y)[0]
    guide_right_face = mount.faces(Select.LAST).filter_by(Axis.X).sort_by(Axis.X, reverse=True)[0]
    tab_edge = guide_face.edges().filter_by(Axis.Z).sort_by(Axis.X)[0]
    with BuildSketch() as tab_sketch:
        with Locations(tab_edge.start_point()):
            Rectangle(
                tab_support_width, tab_gap,
                align=(Align.MIN, Align.MAX))
            with Locations((0, -tab_gap)):
                Rectangle(
                    tab_support_width + tab_length, tab_thickness,
                    align=(Align.MIN, Align.MAX))
        chamfer_point = (
            tab_sketch.vertices()
            .sort_by(Axis.X, reverse=True)[0:2]
            .sort_by(Axis.Y, reverse=True)[0]
        )
        chamfer(chamfer_point, tab_thickness, tab_chamfer_depth)
    extrude(amount=main_height)

    guide_edge = (
        mount.edges().filter_by(Axis.Z)
        .sort_by_distance(
            mount_face.center()
            + (guide_outer_width/2, 0, 0))
    )[0]
    tab_support_edge = (
        mount.edges().filter_by(Axis.Z)
        .sort_by_distance(
            mount_face.center()
            - (guide_outer_width/2 + tab_support_width, 0, 0))
    )[0]

    chamfer(guide_edge, guide_thickness - 0.0001)
    chamfer(tab_support_edge, guide_thickness + tab_gap + tab_thickness - 0.0001)

    with BuildSketch(mount_face) as cutout_sketch:
        with Locations((cutout_horizontal_offset, mount_face.center().Z - main_height/2 -_cutout_vertical_offset)):
            Rectangle(cutout_width, cutout_height)
        chamfer(cutout_sketch.vertices(), 0.8)
    extrude(
        amount=-thickness, mode=Mode.SUBTRACT,
        taper=-cutout_taper
    )
    with BuildSketch(mount_face) as cutout_support_sketch:
        with Locations((cutout_horizontal_offset, mount_face.center().Z - main_height/2 -_cutout_vertical_offset)):
            Rectangle(
                cutout_width - window_support_gap*2,
                cutout_height - support_gap*2,
            )
    extrude(
        amount=-thickness, taper=-cutout_taper
    )
    with BuildSketch(mount_face.offset(support_gap)) as guide_support_sketch:
        with Locations((0, mount_face.center().Z - main_height/2 + pcb_vertical_offset)):
            Rectangle(
                _pcb_width - 2*window_support_gap,
                _pcb_height - 2*support_gap
            )
            Rectangle(
                guide_support_hole_width, guide_support_hole_width,
                mode=Mode.SUBTRACT
            )
    extrude(
        amount=guide_thickness - support_gap - tab_gap
    )
    guide_support_chamfer_edge = (
        mount.edges(Select.LAST).filter_by(Axis.Z)
        .sort_by(Axis.X, reverse=True)[0:2].sort_by(Axis.Y, reverse=True)[0]
    )
    chamfer(
        guide_support_chamfer_edge,
        length=guide_thickness - support_gap - tab_gap - 0.0001,
        length2=guide_support_chamfer_depth,
    )
    with BuildSketch(guide_right_face.offset(-guide_thickness - clip_offset)) as clip_sketch:
        with Locations((0, -guide_thickness/2)):
            Rectangle(main_height, clip_thickness, align=(Align.CENTER, Align.MAX))
        # BuildLine doesn't inherit Locations
        with BuildLine() as path:
            PolarLine(
                (
                    _pcb_height/2 - clip_overhang,
                    -guide_thickness/2
                ),
                angle=-90 + clip_chamfer_angle,
                length=clip_thickness*3
            )
        with BuildLine() as profile:
            PolarLine(
                (
                    _pcb_height/2 - clip_overhang,
                    -guide_thickness/2
                ),
                angle=180,
                length=support_gap
            )
        mirror(
            sweep(profile.line, path.line, mode=Mode.SUBTRACT),
            about=Plane(Location((0, 0, 0), (0, -90, 0))),
            mode=Mode.SUBTRACT
        )
    extrude(amount=-clip_width)

result = mount.part

if __name__ == "__main__":
    if "show_object" in locals():
        show_object(bracket)

    try:
        from ocp_vscode import *
        show_all(reset_camera=Camera.KEEP)
    except ImportError:
        pass

