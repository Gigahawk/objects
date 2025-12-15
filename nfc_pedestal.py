"""Stand for displaying a Pokeball Easycard like this one:
https://cdhelp.iecoach.rest/index.php?main_page=product_info&products_id=344818

Non-printed BOM:
- 1x DLP Design DLP-RFID2
- 1x Adafruit 4090 USB C Breakout Board
    - Aliexpress knockoffs should work as well
- 1x M2.5x40mm socket head screw
- 4x M2.5x6mm socket head screw
- 5x M2.5 square nut

Print settings:
- Support on build plate only
- Remember to insert print pauses to place nuts
- Use the layer height defined below

Notes:
- Initially, my DLP-RFID2 would shut down after powering the Pokeball for a
  short time, and seemingly would not turn back on until power cycled.
  Eventually with enough power cycles it would stay on permanently.
  I have no idea why this happens but I've seen the same behavior on two
  different units so presumably it is consistent.
  Perhaps there is some way of configuring this through the serial connection
  but I have not looked into it
- Choose more dark/opaque filaments to hide the circuit boards under the
  topsheet
- The Aliexpress USB C breakout boards seem to have worse edgecut tolerance than
  the official Adafruit ones, some filing may be required.
  Alternatively, adjust `usb_conn_tol`, but note that the mounting holes on the
  board are drilled and will usually have significantly better tolerance than the
  edge cut.
"""

import copy

from build123d import *

from vitamins import dlp_rfid2
from vitamins import adafruit_4090_usb_c_breakout as usb_breakout
from vitamins import nut_m2_5_square as nut
from vitamins import screw_socket_m2_5_40 as pole_screw
from vitamins import screw_socket_m2_5_06 as base_screw

layer_height = 0.2

# First layer is always 0.2
topsheet_thickness = 0.2 + layer_height
base_width = 70
base_top_thickness = 6
base_fillet = 10

skirt_wall_thickness = 1
skirt_depth = 1
skirt_gap = 4
skirt_tol = 0.1
base_mid_thickness = skirt_gap + skirt_depth

screw_hole_dist_x = 54
screw_hole_dist_y = 58

screw_hole_thread_dia = pole_screw.shank_radius * 2 + 0.1
screw_counter_bore_radius = pole_screw.head_radius * 2 + 0.1
screw_counter_bore_depth = pole_screw.head_height + 0.1
screw_hole_end_ofst_from_surface = 1

pcb_xy_tol = 0.2
dlp_offset = 10
usb_conn_wall_thickness = 0.8
usb_conn_center_offset = 15
usb_conn_tol = 0.2
usb_cc_tol = 0.4

nut_ofst_from_surface = 2
nut_width_tol = 0.2
nut_thickness_tol = 0.2
_nut_cutout = nut.build_cutout(
    width_tol=nut_width_tol,
    thickness_tol=nut_thickness_tol,
    layer_height=layer_height,
    bridge_helper_hole_dia=screw_hole_thread_dia,
)

# TODO: find actual height from pokeball
pole_hook_height = 135
pole_hook_inner_dia = 5
pole_hook_thickness = 2
pole_thickness = 7
pole_width = 7
pole_height = pole_hook_height + pole_hook_inner_dia + pole_thickness / 2
pole_fillet_rad = 30
pole_mount_offset = 27
pole_tol = 0.1
pole_mount_depth = 4
pole_nut_height = 27


_usb_breakout = copy.copy(usb_breakout.out)
_dlp_rfid2 = copy.copy(dlp_rfid2.out)
_pole_screw = copy.copy(pole_screw.out)

_screw_hole_grid_locs = GridLocations(
    x_spacing=screw_hole_dist_x,
    y_spacing=screw_hole_dist_y,
    x_count=2,
    y_count=2,
    align=Align.CENTER,
)

with BuildPart() as base_top:
    with BuildSketch() as base_outer_sketch:
        RectangleRounded(base_width, base_width, base_fillet)
    extrude(base_outer_sketch.sketch, amount=topsheet_thickness)
    extrude(base_outer_sketch.sketch, amount=-base_top_thickness)

    bot_face = base_top.faces().filter_by(Axis.Z).sort_by(Axis.Z)[0]

    with BuildSketch() as dlp_cutout_sketch:
        with Locations((dlp_offset, 0)):
            Rectangle(
                dlp_rfid2.pcb_width + pcb_xy_tol, dlp_rfid2.pcb_height + pcb_xy_tol
            )
        dlp_wiring_edge = (
            dlp_cutout_sketch.sketch.edges().filter_by(Axis.Y).sort_by(Axis.X)[0]
        )
    extrude(dlp_cutout_sketch.sketch, amount=-base_top_thickness, mode=Mode.SUBTRACT)

    usb_breakout_zero = (
        -base_width / 2 + usb_conn_wall_thickness + usb_breakout.pcb_height,
        usb_conn_center_offset + usb_breakout.pcb_width / 2,
        0,
    )

    with BuildSketch() as usb_breakout_sketch:
        with Locations(usb_breakout_zero):
            # Offset after to keep mount hole positions correct
            outline = Rectangle(
                usb_breakout.pcb_height, usb_breakout.pcb_width, align=Align.MAX
            )
        # Don't fillet the corner near VBUS/GND
        no_fillet_point = (
            outline.vertices().sort_by(Axis.X, reverse=True)[0:2].sort_by(Axis.Y)[0]
        )
        fillet_points = outline.vertices()
        fillet_points.remove(no_fillet_point)
        fillet(fillet_points, radius=usb_breakout.pcb_fillet_rad)

        offset(amount=pcb_xy_tol / 2, kind=Kind.INTERSECTION, mode=Mode.REPLACE)
        usb_wiring_edge = (
            usb_breakout_sketch.sketch.edges().filter_by(Axis.Y).sort_by(Axis.X)[-1]
        )

    extrude(usb_breakout_sketch.sketch, amount=-base_top_thickness, mode=Mode.SUBTRACT)

    with BuildSketch() as usb_mount_hole_sketch:
        with Locations(usb_breakout_zero):
            with Locations(
                *(
                    (-c.Y, -c.X)
                    for c in (h.arc_center for h in usb_breakout.mount_holes)
                )
            ):
                Circle(usb_breakout.mount_hole_rad - pcb_xy_tol / 2)
    extrude(usb_mount_hole_sketch.sketch, amount=-usb_breakout.nom_pcb_thickness)

    with BuildSketch() as wiring_sketch:
        with BuildLine():
            wiring_outline = Polyline(
                [
                    dlp_wiring_edge @ 1,
                    # Need access to pins 4-7 for PWR/GND
                    dlp_wiring_edge @ (1 - (4 / 7 + 0.1)),
                    usb_wiring_edge @ 0,
                    # Arbitrary, only need access to last two pins, give extra space for ease of soldering
                    usb_wiring_edge @ 0.4,
                ],
                close=True,
            )
        make_face()
    extrude(wiring_sketch.sketch, amount=-base_top_thickness, mode=Mode.SUBTRACT)

    with BuildSketch(
        Plane.XY.offset(-usb_breakout.nom_pcb_thickness)
    ) as usb_conn_hole_sketch:
        with Locations(usb_breakout_zero):
            with Locations((-usb_breakout.pcb_height / 2, 0)):
                Rectangle(
                    usb_breakout.pcb_height, usb_breakout.pcb_width, align=Align.MAX
                )
        offset(amount=pcb_xy_tol / 2, kind=Kind.INTERSECTION, mode=Mode.REPLACE)
    extrude(usb_conn_hole_sketch.sketch, amount=-base_top_thickness, mode=Mode.SUBTRACT)

    with BuildSketch(bot_face) as skirt_sketch:
        add(bot_face)
        offset(amount=-skirt_wall_thickness, mode=Mode.REPLACE)
    extrude(skirt_sketch.sketch, amount=-skirt_depth, mode=Mode.SUBTRACT)

    with _screw_hole_grid_locs:
        _screw_tip_loc = Location(
            (0, 0, topsheet_thickness - screw_hole_end_ofst_from_surface), (180, 0, 0)
        )
        with Locations(_screw_tip_loc):
            Cylinder(
                radius=screw_hole_thread_dia / 2,
                height=base_top_thickness,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
                mode=Mode.SUBTRACT,
            )
            with Locations(
                (0, 0, nut_ofst_from_surface - screw_hole_end_ofst_from_surface)
            ):
                add(_nut_cutout, mode=Mode.SUBTRACT)
        #    screw_hole = CounterBoreHole(
        #        radius=screw_hole_thread_dia / 2,
        #        depth = base_top_thickness + topsheet_thickness,
        #        counter_bore_radius=screw_counter_bore_radius / 2,
        #        counter_bore_depth=screw_counter_bore_depth,
        #    )

    with BuildSketch() as pole_mount_pocket:
        with Locations((-pole_mount_offset, 0)):
            Rectangle(
                pole_thickness + pole_tol, pole_width + pole_tol, align=Align.CENTER
            )
    extrude(
        pole_mount_pocket.sketch,
        amount=pole_mount_depth,
        # Set both to punch through top sheet
        both=True,
        mode=Mode.SUBTRACT,
    )
    with Locations((-pole_mount_offset, 0)):
        Hole(radius=screw_hole_thread_dia / 2, depth=base_top_thickness)

    for idx, gl in enumerate(_screw_hole_grid_locs):
        gl.orientation = Vector(180, 0, 0)
        gl.position += Vector(0, 0, -nut_ofst_from_surface + topsheet_thickness)
        RigidJoint(label=f"base_nut{idx}", joint_location=gl)

    RigidJoint(
        label="usb_breakout_corner",
        joint_location=Location(usb_breakout_zero, (180, 0, 90)),
    )
    RigidJoint(
        label="dlp_center", joint_location=Location((dlp_offset, 0, 0), (180, 0, 0))
    )
    RigidJoint(
        label="base_top_center",
        joint_location=Location((0, 0, -base_top_thickness + skirt_depth)),
    )


base_top.part.joints["usb_breakout_corner"].connect_to(_usb_breakout.joints["corner"])
base_top.part.joints["dlp_center"].connect_to(_dlp_rfid2.joints["center"])
base_nuts = {}
for idx in range(4):
    key = f"base_nut{idx}"
    base_nuts[key] = copy.copy(nut.out)
    base_top.part.joints[key].connect_to(base_nuts[key].joints["bottom"])


with BuildPart() as base_mid:
    with BuildSketch() as skirt_insert_sketch:
        add(skirt_sketch.sketch)
        offset(amount=-skirt_tol / 2, mode=Mode.REPLACE)
    extrude(skirt_insert_sketch.sketch, amount=-(base_mid_thickness))

    RigidJoint(label="base_mid_center", joint_location=Location((0, 0, 0)))

    with BuildSketch(Plane.XY.offset(-skirt_depth)) as usb_clamp_sketch:
        add(bot_face)
        _usb_conn_hole_rect = add(usb_conn_hole_sketch.sketch, mode=Mode.PRIVATE)
        _usb_breakout_rect = add(usb_breakout_sketch.sketch, mode=Mode.PRIVATE)
        with Locations(usb_breakout_zero):
            with Locations((0, -usb_breakout.pcb_width)):
                _pin_clearance_rect = Rectangle(
                    # HACK: idk this probably shouldn't be hardcoded
                    4,
                    usb_wiring_edge.length * 0.4,
                    align=(Align.MAX, Align.MIN),
                    mode=Mode.PRIVATE,
                )
        offset(
            _usb_conn_hole_rect + _usb_breakout_rect - _pin_clearance_rect,
            amount=-skirt_tol / 2,
            mode=Mode.INTERSECT,
        )

        with Locations(usb_breakout_zero):
            cc_bbox = usb_breakout.resistor_bbox
            cc_center = cc_bbox.center()
            with Locations((-cc_center.Y, -cc_center.X)):
                Rectangle(
                    cc_bbox.size.Y + usb_cc_tol,
                    cc_bbox.size.X + usb_cc_tol,
                    mode=Mode.SUBTRACT,
                )

    # TODO: figure out dist?
    extrude(
        usb_clamp_sketch.sketch,
        amount=base_top_thickness - usb_breakout.nom_pcb_thickness,
    )

    with BuildSketch(Plane.YZ.offset(-base_width / 2)) as usb_cutout_sketch:
        with Locations(
            (
                usb_conn_center_offset,
                base_top_thickness - skirt_depth - usb_breakout.nom_pcb_thickness,
            )
        ):
            Rectangle(
                usb_breakout.usb_width + usb_conn_tol,
                usb_breakout.usb_height + usb_conn_tol,
                align=(Align.CENTER, Align.MAX),
            )
        # Broken by https://github.com/gumyr/build123d/issues/314
        fillet_points = usb_cutout_sketch.sketch_local.vertices().sort_by(Axis.Y)[0:2]
        fillet(fillet_points, radius=usb_breakout.usb_fillet_rad)
    extrude(
        usb_cutout_sketch.sketch,
        amount=usb_breakout.usb_depth + usb_conn_wall_thickness + usb_conn_tol,
        mode=Mode.SUBTRACT,
    )

    with BuildSketch() as dlp_clamp_sketch:
        _dlp_sketch = add(dlp_cutout_sketch.sketch, mode=Mode.PRIVATE)
        offset(_dlp_sketch, amount=-skirt_tol / 2, mode=Mode.REPLACE)
    extrude(
        dlp_clamp_sketch.sketch,
        amount=base_top_thickness - skirt_depth - dlp_rfid2.module_total_thickness,
    )

    with _screw_hole_grid_locs:
        _screw_loc = Location(
            (0, 0, -base_mid_thickness),
            (180, 0, 0),
        )
        with Locations(_screw_loc):
            CounterBoreHole(
                radius=screw_hole_thread_dia / 2,
                depth=base_mid_thickness,
                counter_bore_radius=screw_counter_bore_radius / 2,
                counter_bore_depth=screw_counter_bore_depth,
            )

    base_mid_bot = base_mid.faces().filter_by(Axis.Z).sort_by(Axis.Z)[0]
    pole_hole_point = Location(
        base_mid_bot.center() + Vector(-pole_mount_offset, 0, 0), (180, 0, 0)
    )
    with Locations(pole_hole_point):
        pole_mont_cbore = CounterBoreHole(
            radius=screw_hole_thread_dia / 2,
            depth=10,
            counter_bore_radius=screw_counter_bore_radius / 2,
            counter_bore_depth=screw_counter_bore_depth,
        )
    pole_cbore_point = Location(
        base_mid_bot.center() + Vector(-pole_mount_offset, 0, screw_counter_bore_depth),
    )

    for idx, gl in enumerate(_screw_hole_grid_locs):
        gl.position += Vector(0, 0, -base_mid_thickness + screw_counter_bore_depth)
        RigidJoint(label=f"base_screw{idx}", joint_location=gl)

    RigidJoint(label="pole_screw_hole", joint_location=pole_cbore_point)

base_top.part.joints["base_top_center"].connect_to(base_mid.joints["base_mid_center"])
base_mid.part.joints["pole_screw_hole"].connect_to(_pole_screw.joints["head_bottom"])

base_screws = {}
for idx in range(4):
    key = f"base_screw{idx}"
    base_screws[key] = copy.copy(base_screw.out)
    base_mid.part.joints[key].connect_to(base_screws[key].joints["head_bottom"])

with BuildPart() as pole:
    hook_point = Vector(dlp_offset, 0, pole_hook_height)
    with BuildLine() as pole_path:
        Polyline(
            [
                (-pole_mount_offset, 0, -pole_mount_depth),
                (-pole_mount_offset, 0, pole_height),
                (dlp_offset + pole_hook_inner_dia / 2, 0, pole_height),
            ],
        )
        _pole_fillet_corner = (
            pole_path.vertices().sort_by(Axis.Z, reverse=True)[0:2].sort_by(Axis.X)
        )[0]
        fillet(_pole_fillet_corner, radius=pole_fillet_rad)
    with BuildSketch() as pole_profile:
        with Locations((-pole_mount_offset, 0)):
            Rectangle(pole_thickness, pole_width, align=Align.CENTER)
    sweep(sections=pole_profile.sketch, path=pole_path.line)

    with BuildSketch(Plane.XZ) as hook_sketch:
        with Locations((dlp_offset, pole_hook_height + pole_hook_inner_dia / 2)):
            Circle(pole_hook_inner_dia / 2 + pole_hook_thickness)
            Circle(pole_hook_inner_dia / 2, mode=Mode.SUBTRACT)
    extrude(amount=pole_hook_thickness / 2, both=True)

    pole_bot_face = pole.faces().filter_by(Axis.Z).sort_by(Axis.Z)[0]
    with BuildSketch(pole_bot_face) as pole_mount_hole_sketch:
        Circle(screw_hole_thread_dia / 2)
    extrude(
        pole_mount_hole_sketch.sketch,
        # Technically overkill but whatever
        amount=-pole_screw.length,
        mode=Mode.SUBTRACT,
    )

    _pole_nut_loc = Location((-pole_mount_offset, 0, pole_nut_height))
    with Locations(_pole_nut_loc):
        _pole_nut_hole = Box(
            nut.nut_width + nut_width_tol,
            nut.nut_width + nut_width_tol,
            nut.nut_thickness + nut_thickness_tol,
            mode=Mode.SUBTRACT,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        RigidJoint(label="pole_nut", joint_location=_pole_nut_loc)

_pole_nut = copy.copy(nut.out)
pole.part.joints["pole_nut"].connect_to(_pole_nut.joints["bottom"])

asm = Compound([base_top.part, base_mid.part, pole.part])

results = {
    "base_top": base_top.part,
    "base_mid": base_mid.part,
    "pole": pole.part,
    "asm": asm,
}


if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
            render_joints=True,
        )
    except ImportError:
        pass
