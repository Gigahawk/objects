from build123d import *

# From datasheet
# https://www.dlpdesign.com/rf/dlp-rfid2-ds-v114.pdf
pcb_width = 42.7
pcb_height = 18.8
module_total_thickness = 4.3
pin_spacing = 2.54
pin_count = 7  # per side

# From measurements/calculation
pcb_thickness = 1.6
shield_thickness = module_total_thickness - pcb_thickness
shield_width = 32.7
shield_height = 14.8
# From left side of PCB as shown in datasheet
shield_start_x = 3.5
# From top side of PCB as shown in datasheet
shield_start_y = 1.5

ant_conn_width = 2.5
ant_conn_thickness = 1.3
# From right side of PCB as shown in datasheet
ant_conn_start_x = 1.7
# From top side of PCB as shown in datasheet
ant_conn_start_y = 2.85

pin_hole_dia = 0.8
pin_start_x = 0.4 + pin_hole_dia / 2
pin_start_y = 1.3 + pin_hole_dia / 2

with BuildPart() as _out:
    with BuildSketch() as board_sketch:
        Rectangle(pcb_width, pcb_height, align=(Align.MIN, Align.MAX))
    extrude(amount=pcb_thickness)
    pcb_top_face = _out.faces().filter_by(Axis.Z).sort_by(Axis.Z)[-1]

    with BuildSketch(Plane.XY.offset(pcb_thickness)) as shield_sketch:
        with Locations((shield_start_x, -shield_start_y)):
            Rectangle(shield_width, shield_height, align=(Align.MIN, Align.MAX))
    extrude(amount=shield_thickness)

    with BuildSketch(Plane.XY.offset(pcb_thickness)) as ant_conn_sketch:
        with Locations((pcb_width - ant_conn_start_x, -ant_conn_start_y)):
            Rectangle(ant_conn_width, ant_conn_width, align=Align.MAX)
    extrude(amount=ant_conn_thickness)

    with BuildSketch() as hole_sketch:
        with Locations(
            (pin_start_x, -pin_start_y), (pcb_width - pin_start_x, -pin_start_y)
        ):
            with GridLocations(
                x_spacing=0,
                y_spacing=pin_spacing,
                x_count=1,
                y_count=pin_count,
                align=Align.MAX,
            ):
                Circle(radius=pin_hole_dia / 2)
    extrude(amount=pcb_thickness, mode=Mode.SUBTRACT)

    RigidJoint(
        label="center", joint_location=Location((pcb_width / 2, -pcb_height / 2, 0))
    )

out = _out.part
out.color = Color("green")


if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
            render_joints=True,
        )
    except ImportError:
        pass
