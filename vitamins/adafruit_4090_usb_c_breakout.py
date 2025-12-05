from pathlib import Path

from build123d import *

out = import_step(Path(__file__).parent.parent / "res/4090_USB_C_Breakout.step")
out.color = Color("blue")

# HACK: The first two faces happen to be the two PCB faces.
# We can't just sort by Z first because the bottoms of the resistors
# actually sit a little below the top surface
pcb_faces = out.faces().filter_by(Axis.Z)[0:2].sort_by(Axis.Z)
bot_face, top_face = pcb_faces

usb_top_face = out.faces().filter_by(Axis.Z).sort_by(Axis.Z)[-1]
usb_height = usb_top_face.center().Z - top_face.center().Z

# Kind of arbitrary, don't really know of a better way to do this
usb_side_faces = out.faces().filter_by(Axis.X).filter_by(lambda f: f.area > 9.5 and f.area < 10)
usb_side_face_locs = [f.center().X for f in usb_side_faces]
usb_width = abs(usb_side_face_locs[0] - usb_side_face_locs[1])

# Why doesn't just a simple filter_by(Axis.Y) work for this?
usb_fillets = (
    out.faces().filter_by(GeomType.CYLINDER)
    .filter_by(lambda f: f.rotational_axis.is_parallel(Axis.Y))
    .sort_by(lambda f: f.radius, reverse=True)
)[0:6]  # Bottom fillets count for 2 each cause of mounting legs
usb_top_fillets = usb_fillets.sort_by(Axis.Z, reverse=True)[0:2]
usb_fillet_rad = usb_top_fillets[0].radius

nom_pcb_thickness = top_face.center().Z - bot_face.center().Z

outline = bot_face.outer_wire()
pcb_fillets = outline.edges().filter_by(GeomType.CIRCLE)
pcb_fillet_rad = pcb_fillets[0].radius
bbox = outline.bounding_box()
pcb_width, pcb_height, _ = bbox.size
#print(f"pcb_width: {pcb_width}, pcb_height: {pcb_height}, pcb_thickness: {nom_pcb_thickness}, pcb_fillet: {pcb_fillet}")

pcb_holes = bot_face.edges().filter_by(GeomType.CIRCLE).filter_by(lambda e: e.radius != pcb_fillet_rad)
mount_holes = pcb_holes.sort_by(lambda e: e.radius, reverse=True)[0:2]
mount_hole_rad = mount_holes[0].radius

# Kinda hacky way to get the USB pins edge
usb_pin_edge = (
    out.faces().filter_by(GeomType.PLANE)
    .filter_by(Axis.Y)
    .sort_by(Axis.Y)
)[6]
usb_depth = pcb_height - usb_pin_edge.center().Y
#print(usb_depth)

# Kinda hacky to get the CC resistors locations
resistor_y_edge_1 = (
    out.faces().filter_by(GeomType.PLANE)
    .filter_by(Axis.Y)
    .sort_by(Axis.Y)
)[3]
resistor_height = resistor_y_edge_1.length

resistor_y_edges = (
    out.faces().filter_by(GeomType.PLANE)
    .filter_by(Axis.Y)
    # Need some tolerance for this to work
    .filter_by(lambda f: abs(f.area - resistor_y_edge_1.area) < 0.01)
)
resistor_y_edge_2 = resistor_y_edges.sort_by(Axis.Y)[-1]

resistor_x_edge_1 = (
    out.faces().filter_by(GeomType.PLANE)
    .filter_by(Axis.X)
    .sort_by(Axis.X)
)[1]

resistor_x_edges = (
    out.faces().filter_by(GeomType.PLANE)
    .filter_by(Axis.X)
    # Need some tolerance for this to work
    .filter_by(lambda f: abs(f.area - resistor_x_edge_1.area) < 0.01)
)

resistor_x_edge_2 = resistor_x_edges.sort_by(Axis.X)[-1]
resistor_edges = Compound(
    [resistor_x_edge_1, resistor_x_edge_2, resistor_y_edge_1, resistor_y_edge_2]
)
resistor_bbox = resistor_edges.bounding_box()


corner_joint = RigidJoint(label="corner", joint_location=Location((0,0,0)), to_part=out)

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
            render_joints=True
        )
    except ImportError:
        pass
