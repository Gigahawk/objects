"""Holder for Predator 1080 Chalk"""
from build123d import *
from bd_warehouse.thread import Thread



outer_dia = 29
thread_min_dia = 27.5
thread_maj_dia = 28.5
thread_pitch = 1
thread_tol = 0.1
thread_depth = 3
thread_tip_width = 0.2
# Must be non zero to avoid weird OCP issues
thread_interference = 0.0001

end_thickness = 1
lower_depth = 6.5
face_to_face_dist = 24.578
clearance_hole_dia = 20

total_internal_height = 21

lower_total_height = lower_depth + end_thickness
lower_unthreaded_height = lower_total_height - thread_depth
thread_root_width = thread_pitch - thread_tip_width - thread_tol
upper_internal_height = total_internal_height - lower_total_height

_lower_thread = Thread(
    apex_radius=thread_maj_dia/2 - thread_tol,
    apex_width=thread_tip_width,
    root_radius=thread_min_dia/2,
    root_width=thread_root_width,
    interference=thread_interference,
    pitch=thread_pitch,
    length=thread_depth,
    end_finishes=["fade","fade"]
)
_upper_thread = Rotation(0, 0, 180) * Thread(
    apex_radius=thread_maj_dia/2,
    apex_width=thread_root_width,
    root_radius=thread_min_dia/2 - thread_tol,
    root_width=thread_tip_width,
    interference=thread_interference,
    pitch=thread_pitch,
    length=thread_depth,
    end_finishes=["fade","fade"]
)


with BuildPart() as lower:
    add(_lower_thread)
    Cylinder(
        thread_min_dia/2 - thread_interference, thread_depth - thread_tol,
        align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    Cylinder(
        outer_dia/2, lower_unthreaded_height,
        align=(Align.CENTER, Align.CENTER, Align.MAX)
    )
    top_face = lower.faces().sort_by(Axis.Z, reverse=True)[0]
    with BuildSketch(top_face):
        RegularPolygon(side_count=8, radius=face_to_face_dist/2, major_radius=False)
    extrude(amount=-lower_depth, mode=Mode.SUBTRACT)
    with BuildSketch():
        Circle(radius=clearance_hole_dia/2)
    extrude(amount=-lower_unthreaded_height, mode=Mode.SUBTRACT)

with BuildPart() as upper:
    add(_upper_thread)
    with BuildSketch():
        Circle(radius=outer_dia/2)
        Circle(radius=thread_maj_dia/2 - thread_interference, mode=Mode.SUBTRACT)
    extrude(amount=thread_depth)
    top_face = upper.faces().sort_by(Axis.Z, reverse=True)[0]
    with BuildSketch(top_face):
        Circle(radius=outer_dia/2)
        Circle(radius=thread_min_dia/2, mode=Mode.SUBTRACT)
    extrude(amount=upper_internal_height)
    #inner_edge = upper.edges(select=Select.LAST).filter_by(GeomType.CIRCLE).sort_by(Axis.Z).sort_by(SortBy.RADIUS)[0]
    inner_edge = upper.edges(select=Select.LAST).filter_by(GeomType.CIRCLE).sort_by(SortBy.RADIUS)[:2].sort_by(Axis.Z)[0]
    # TODO: update to b3d 0.9
    #chamfer_len1 = max_fillet(inner_edge)
    chamfer_len1 = (thread_maj_dia - thread_min_dia)/2 - 0.01
    #chamfer(inner_edge, 0.45, 3)
    chamfer(inner_edge, chamfer_len1, 3)
    top_face = upper.faces().sort_by(Axis.Z, reverse=True)[0]
    with BuildSketch(top_face):
        Circle(radius=outer_dia/2)
    extrude(amount=end_thickness)
    
    

results = {
    "lower": lower.part,
    "upper": upper.part
}

if __name__ == "__main__":
    try:
        from ocp_vscode import *
        show_all(
            reset_camera=Camera.KEEP,
        )
    except ImportError:
        pass
    
