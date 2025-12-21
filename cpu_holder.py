"""Holder for various CPU types

Currently supports CPUs for the following sockets:
- FCPGA946

Print setting recommendations:
- Brim ears on corners (Superslicer feature)
    - Use brim blockers on the inside corners between the two
      halves fusing them together
- Support on build plate only
    - Block supports inside the hinge
- Print the tab on its side with no brim
"""

from build123d import *

from vitamins import hinge

hinge_gap = 0.2
hinge_dia = 10
hinge_ground_gap = 1

clamshell_thickness = hinge_dia / 2 + hinge_ground_gap
clamshell_wall_thickness = 2

cpu_substrate_width = 37.5
cpu_substrate_height = 37.5
cpu_substrate_thickness = 1.2
cpu_pin_margin_x = 1
cpu_pin_margin_y = 0.8
cpu_pin_depth = 2
cpu_heatspreader_width = 25
cpu_heatspreader_height = 30
# To compensate for interference with hinge
cpu_heatspreader_chamfer = 3
# To compensate for printer internal radii
cpu_corner_cutout_rad = 0.5

cpu_xy_tol = 0.25
cpu_z_tol = 0.1

label_extra = 5
finger_gap_length = 15
finger_gap_taper_angle = 20
marker_depth = 1
marker_width = clamshell_wall_thickness / 1.5

# Max width for PrusaSlicer to not complain about a long bridge is about 14.5
tab_width = 12
tab_catch_depth = 1.6
tab_thickness = 1
tab_mount_hole_depth = 10
tab_mount_hole_width_tol = 0.2
tab_mount_hole_thickness_tol = 0.4
tab_mount_hole_depth_tol = 0.05
tab_fillet_rad = 2
tab_end_height_tol = 1
tab_end_chamfer = 0.8

_cpu_substrate_width = cpu_substrate_width + cpu_xy_tol
_cpu_substrate_length = cpu_substrate_height + cpu_xy_tol
_cpu_substrate_thickness = cpu_substrate_thickness + cpu_z_tol
_cpu_pin_depth = cpu_pin_depth + cpu_z_tol
_cpu_heatspreader_width = cpu_heatspreader_width + cpu_xy_tol
_cpu_heatspreader_height = cpu_heatspreader_height + cpu_xy_tol

clamshell_length = (
    hinge_dia / 2 + _cpu_substrate_length + 2 * clamshell_wall_thickness + label_extra
)
hinge_width = _cpu_substrate_width + 2 * clamshell_wall_thickness
cpu_pin_pocket_width = _cpu_substrate_width - 2 * cpu_pin_margin_x
cpu_pin_pocket_length = _cpu_substrate_length - 2 * cpu_pin_margin_y
tab_hole_height = (
    clamshell_thickness - (_cpu_substrate_thickness + _cpu_pin_depth)
) / 2
tab_hole_height_rem = clamshell_thickness - tab_hole_height
# When printing we expect the top layer to droop pushing the tab into the bottom
# of the hole, move path down to compensate so we end up with the correct length
tab_thickness_center_offset = tab_mount_hole_thickness_tol/2

_hinge = hinge.build(
    hinge_dia=hinge_dia,
    hinge_width=hinge_width,
    hinge_gap=hinge_gap,
)

assert tab_mount_hole_width_tol > 0
assert tab_mount_hole_thickness_tol > 0
assert tab_mount_hole_depth_tol > 0

hinge_center_loc = Vector(-hinge_width / 2, 0, clamshell_thickness)
clamshell_offset = Vector(0, hinge_gap / 2, 0)
rotation_axis = Axis.X.located(Location(hinge_center_loc))

with BuildPart() as holder_parent:
    with Locations(-clamshell_offset):
        Box(
            hinge_width,
            clamshell_length,
            clamshell_thickness,
            align=(Align.CENTER, Align.MAX, Align.MIN),
        )
    parent_top_face = holder_parent.part.faces().filter_by(Axis.Z).sort_by(Axis.Z)[-1]
    parent_front_face = holder_parent.part.faces().filter_by(Axis.Y).sort_by(Axis.Y)[0]
    parent_front_edge = parent_top_face.edges().filter_by(Axis.X).sort_by(Axis.Y)[0]
    parent_center_loc = Location(
        parent_front_edge.center()
        + Vector(0, clamshell_wall_thickness + _cpu_substrate_length / 2, 0)
    )
    parent_tab_hole_loc = Location(
        parent_front_edge.center()
        + Vector(0, 0, (-clamshell_thickness + tab_hole_height))
    )
    with BuildSketch(parent_center_loc) as marker_sketch:
        marker_loc = Location(
            (
                -(_cpu_substrate_width / 2),
                (_cpu_substrate_length / 2 + clamshell_wall_thickness / 2),
                0,
            )
        )
        with Locations(marker_loc):
            Triangle(
                a=marker_width,
                b=marker_width,
                C=90,
                align=(Align.MIN, Align.MAX),
                rotation=180,
            )
    extrude(amount=-marker_depth, mode=Mode.SUBTRACT)

    with BuildSketch(parent_center_loc) as substrate_pocket_sketch:
        Rectangle(
            _cpu_substrate_width,
            _cpu_substrate_length,
        )
        _corners = substrate_pocket_sketch.vertices()
        with Locations(_corners):
            Circle(cpu_corner_cutout_rad)
    extrude(amount=-_cpu_substrate_thickness, mode=Mode.SUBTRACT)

    substrate_pocket_face = (
        holder_parent.faces(Select.LAST).filter_by(Axis.Z).sort_by(Axis.Z)[0]
    )

    with BuildSketch(parent_center_loc) as substrate_pocket_sketch:
        Rectangle(
            _cpu_substrate_width + 2 * clamshell_wall_thickness, finger_gap_length
        )
        Rectangle(
            _cpu_substrate_width,
            _cpu_substrate_length,
            mode=Mode.SUBTRACT,
        )
    extrude(amount=-_cpu_substrate_thickness, mode=Mode.SUBTRACT)

    with BuildSketch(substrate_pocket_face) as pin_pocket_sketch:
        Rectangle(
            cpu_pin_pocket_width,
            cpu_pin_pocket_length,
        )
    extrude(amount=-_cpu_pin_depth, mode=Mode.SUBTRACT)

    with BuildSketch(substrate_pocket_face) as substrate_pocket_sketch:
        Rectangle(
            # Just a really big value to ensure we cut all the way through even with a taper
            (_cpu_substrate_width + 2 * clamshell_wall_thickness)*2,
            finger_gap_length
        )
        Rectangle(
            _cpu_substrate_width,
            _cpu_substrate_length,
            mode=Mode.SUBTRACT,
        )
    extrude(
        amount=-clamshell_thickness,
        mode=Mode.SUBTRACT,
        taper=finger_gap_taper_angle
    )


    with BuildSketch(parent_front_face) as tab_hole_sketch:
        with Locations(Location((0, 0, 0), (0, 0, -90))):
            with Locations((0, -clamshell_thickness / 2 + tab_hole_height)):
                Rectangle(
                    tab_width + tab_mount_hole_width_tol,
                    tab_thickness + tab_mount_hole_thickness_tol,
                )
    extrude(
        amount=-(tab_mount_hole_depth + tab_mount_hole_depth_tol), mode=Mode.SUBTRACT
    )

    with Locations(hinge_center_loc):
        add(_hinge["parent_cutout"], mode=Mode.SUBTRACT)
        add(_hinge["parent"])

with BuildPart() as _tab:
    with BuildLine() as tab_path:
        _base_line = FilletPolyline(
            [
                (0, tab_mount_hole_depth, -tab_thickness_center_offset),
                (0, -(tab_catch_depth + tab_thickness / 2), -tab_thickness_center_offset),
                (
                    0,
                    -(tab_catch_depth + tab_thickness / 2),
                    tab_hole_height_rem + clamshell_thickness - tab_end_height_tol,
                ),
            ],
            radius=tab_fillet_rad,
            mode=Mode.PRIVATE,
        ).moved(parent_tab_hole_loc)
        add(_base_line)

    with BuildSketch(parent_front_face, mode=Mode.PRIVATE) as tab_profile:
        with Locations(Location((0, 0, 0), (0, 0, -90))):
            with Locations(
                (0, -clamshell_thickness / 2 + tab_hole_height - tab_thickness_center_offset)
            ):
                Rectangle(
                    tab_width,
                    tab_thickness,
                )
    sweep(sections=tab_profile.sketch, path=tab_path.line)
    tab_top_edge = (
        _tab.edges(Select.LAST)
        .filter_by(Axis.X)
        .sort_by(Axis.Z, reverse=True)[0:2]
        .sort_by(Axis.Y)[-1]
    )

    with BuildSketch(Plane.YZ) as parent_tab_catch_sketch:
        _tab_parent_catch_sketch_local_loc = Location(
            (
                tab_top_edge.center().Y,
                tab_top_edge.center().Z,
            )
        )
        with Locations(_tab_parent_catch_sketch_local_loc):
            _catch_height = clamshell_thickness / 2 - tab_end_height_tol
            Triangle(
                a=_catch_height,
                b=tab_catch_depth,
                C=90,
                align=(Align.MIN, Align.MIN),
                rotation=-90,
            )
            with Locations((tab_catch_depth, -_catch_height)):
                tab_chamfer_cut = Triangle(
                    a=tab_end_chamfer,
                    b=tab_end_chamfer,
                    C=90,
                    mode=Mode.SUBTRACT,
                    rotation=0,
                    align=(Align.MAX, Align.MIN),
                )
    extrude(amount=tab_width / 2, both=True)


with BuildPart() as holder_child:
    with Locations(clamshell_offset):
        Box(
            hinge_width,
            clamshell_length,
            clamshell_thickness,
            align=(Align.CENTER, Align.MIN, Align.MIN),
        )
    child_top_face = holder_child.part.faces().sort_by(Axis.Z)[-1]
    child_front_edge = child_top_face.edges().filter_by(Axis.X).sort_by(Axis.Y)[-1]
    child_center_loc = Location(
        child_front_edge.center()
        - Vector(0, clamshell_wall_thickness + _cpu_substrate_length / 2, 0)
    )
    child_tab_loc = Location(
        child_front_edge.center() - Vector(0, 0, clamshell_thickness / 2)
    )

    with BuildSketch(child_center_loc) as heatspreader_pocket_sketch:
        Rectangle(
            _cpu_heatspreader_width,
            _cpu_heatspreader_height,
        )
    extrude(amount=-clamshell_thickness, mode=Mode.SUBTRACT)

    heatspreader_chamfer_edges = (
        holder_child.edges(Select.LAST)
        .filter_by(Axis.X)
        .sort_by(Axis.Z, reverse=True)[0:2]
    )
    chamfer(heatspreader_chamfer_edges, length=cpu_heatspreader_chamfer)

    with BuildSketch(Plane.YZ) as tab_catch_sketch:
        _tab_catch_sketch_local_loc = Location(
            (
                child_tab_loc.position.Y,
                child_tab_loc.position.Z,
            )
        )
        with Locations(_tab_catch_sketch_local_loc):
            Triangle(
                a=clamshell_thickness / 2,
                b=tab_catch_depth,
                C=90,
                align=(Align.MAX, Align.MIN),
                rotation=-90,
            )
    extrude(amount=tab_width / 2, both=True)

    with Locations(hinge_center_loc):
        add(_hinge["child_cutout"], mode=Mode.SUBTRACT)
        add(_hinge["child"])

holder_child_rotated = holder_child.part.rotate(rotation_axis, 180)


results = {
    "asm_print": Compound([holder_parent.part, holder_child.part]),
    "asm_rotated": Compound([holder_parent.part, holder_child_rotated]),
    "tab": _tab.part,
}


if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(reset_camera=Camera.KEEP, render_joints=True)
    except ImportError:
        pass
