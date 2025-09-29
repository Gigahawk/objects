"""Holder for Predator 1080 Chalk"""
from build123d import *
from bd_warehouse.thread import Thread
#from bd_warehouse.thread import IsoThread
from math import sin, cos, radians, tan



outer_dia = 34
thread_min_dia = 27.5
thread_maj_dia = 29
thread_pitch = 2
thread_tol = 0.1
thread_depth = 4
thread_tip_width = 0.2
# Must be non zero to avoid weird OCP issues
thread_interference = 0.0001

end_thickness = 1.5
end_chamfer = 1
lower_depth = 6.5
face_to_face_dist = 24.678
clearance_hole_dia = 20
total_internal_height = 23

keyring_outer_dia = 7
keyring_inner_dia = 5
keyring_angle = 40  # Angle between tangent lines from keyring
keyring_center_dist = 20
keyring_thickness = 2

lower_total_height = lower_depth + end_thickness
lower_unthreaded_height = lower_total_height - thread_depth
thread_root_width = thread_pitch - thread_tip_width - thread_tol
upper_internal_height = total_internal_height - lower_total_height
flat_width = thread_maj_dia + (outer_dia - thread_maj_dia)/2
upper_total_height = upper_internal_height + thread_depth + end_thickness + thread_tol

# Ugly trig for figuring out keyring geom, probably not the most efficient way to do this
phi = keyring_angle/2
theta = 90 - phi
r = keyring_outer_dia/2
l1 = r*sin(radians(phi))
h1 = r*cos(radians(phi))
l2 = h1*tan(radians(theta))
l = keyring_center_dist + l1 + l2
h = l/tan(radians(theta))
keyring_pts = [
    (0, h),
    (l, 0),
    (0, -h)
]

_lower_thread = Thread(
    apex_radius=thread_maj_dia/2 - thread_tol,
    apex_width=thread_tip_width,
    root_radius=thread_min_dia/2 - thread_tol,
    root_width=thread_root_width,
    pitch=thread_pitch,
    length=thread_depth,
    end_finishes=["fade","fade"]
)
_upper_thread = Rotation(0, 0, 180) * Thread(
    apex_radius=thread_min_dia/2 + thread_tol,
    apex_width=thread_tip_width,
    root_radius=thread_maj_dia/2 + thread_tol,
    root_width=thread_root_width,
    pitch=thread_pitch,
    length=thread_depth,
    end_finishes=["fade","fade"]
)

#_lower_thread = IsoThread(
#    major_diameter=thread_maj_dia - thread_tol,
#    pitch=thread_pitch,
#    length=thread_depth,
#    external=True,
#    end_finishes=["fade","fade"]
#)
#_upper_thread = Rotation(0, 0, 180) * IsoThread(
#    major_diameter=thread_maj_dia + thread_tol,
#    pitch=thread_pitch,
#    length=thread_depth,
#    external=False,
#    interference=0,
#    end_finishes=["fade","fade"]
#)
#thread_min_dia = _lower_thread.min_radius*2


with BuildPart() as _lower:
    Cylinder(
        thread_min_dia/2 - thread_interference, thread_depth - thread_tol,
        align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    Cylinder(
        outer_dia/2, lower_unthreaded_height,
        align=(Align.CENTER, Align.CENTER, Align.MAX)
    )
    bottom_face = _lower.faces().sort_by(Axis.Z)[0]
    bottom_edge = bottom_face.edges()
    chamfer(bottom_edge, end_chamfer)
    top_face = _lower.faces().sort_by(Axis.Z, reverse=True)[0]

    top_face = _lower.faces().sort_by(Axis.Z, reverse=True)[0]
    with BuildSketch(top_face) as flat_sketch:
        RegularPolygon(side_count=8, rotation=360/8/2, radius=flat_width/2, major_radius=False)
    extrude(amount=-lower_total_height, mode=Mode.INTERSECT)
    with BuildSketch(bottom_face) as keyring_sketch:
        with BuildLine():
            FilletPolyline(keyring_pts, radius=keyring_outer_dia/2, close=True)
        make_face()
        with Locations((keyring_center_dist, 0)):
            Circle(radius=keyring_inner_dia/2, mode=Mode.SUBTRACT)
    extrude(amount=-keyring_thickness)
    with BuildSketch(top_face):
        RegularPolygon(side_count=8, rotation=360/8/2, radius=face_to_face_dist/2, major_radius=False)
    extrude(amount=-lower_depth, mode=Mode.SUBTRACT)
    with BuildSketch():
        Circle(radius=clearance_hole_dia/2)
    extrude(amount=-lower_unthreaded_height, mode=Mode.SUBTRACT)

lower = Compound([_lower.part, _lower_thread])

with BuildPart() as _upper:
    with BuildSketch(Plane.XY) as thread_outer_sketch:
        Circle(radius=outer_dia/2)
        Circle(radius=thread_maj_dia/2 + thread_tol, mode=Mode.SUBTRACT)
    extrude(amount=thread_depth + thread_tol)
    top_face = _upper.faces().sort_by(Axis.Z, reverse=True)[0]
    with BuildSketch(top_face):
        Circle(radius=outer_dia/2)
        Circle(radius=thread_min_dia/2, mode=Mode.SUBTRACT)
    extrude(amount=upper_internal_height)
    inner_edge = _upper.edges(select=Select.LAST).filter_by(GeomType.CIRCLE).sort_by(SortBy.RADIUS)[:2].sort_by(Axis.Z)[0]
    # TODO: update to b3d 0.9
    #chamfer_len1 = max_fillet(inner_edge)
    chamfer_len1 = (thread_maj_dia + thread_tol - thread_min_dia)/2 - 0.01
    #chamfer(inner_edge, 0.45, 3)
    chamfer(inner_edge, chamfer_len1, 3)
    top_face = _upper.faces().sort_by(Axis.Z, reverse=True)[0]
    with BuildSketch(top_face):
        Circle(radius=outer_dia/2)
    extrude(amount=end_thickness)
    top_face = _upper.faces().sort_by(Axis.Z, reverse=True)[0]
    chamfer(top_face.edges(), end_chamfer)
    with BuildSketch(top_face) as flat_sketch:
        RegularPolygon(side_count=8, rotation=360/8/2, radius=flat_width/2, major_radius=False)
    extrude(amount=-upper_total_height, mode=Mode.INTERSECT)
upper = Compound([_upper.part, _upper_thread])
    
    

results = {
    "lower": lower,
    "upper": upper,
}

if __name__ == "__main__":
    try:
        from ocp_vscode import *
        show_all(
            reset_camera=Camera.KEEP,
        )
    except ImportError:
        pass
    
