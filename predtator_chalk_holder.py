"""Holder for Predator 1080 Chalk"""

from build123d import *
from bd_warehouse.thread import Thread

from math import sin, cos, radians, tan


outer_dia = 37
thread_min_dia = 28.5
thread_maj_dia = 30
thread_pitch = 2
thread_tol = 0.1
thread_depth = 4
thread_tip_width = 0.2
thread_compliment_rotation = (
    180 + 22.5  # Extra to ensure faces line up when threads are tight
)

bottom_thickness = 6
top_thickness = 1
end_chamfer = 2
upper_inner_chamfer_length = 10
lower_depth = 6.5
face_to_face_dist = 24.678
clearance_hole_dia = 20
total_internal_height = 22
finger_indent_depth = 1
# TODO: refactor to allow this to be smaller than keyring_thickness
finger_indent_margin = 1.5

keyring_outer_dia = 7
keyring_inner_dia = 5
keyring_angle = 40  # Angle between tangent lines from keyring
keyring_center_dist = 20
keyring_thickness = 3

lower_total_height = lower_depth + bottom_thickness
lower_unthreaded_height = lower_total_height - thread_depth
thread_root_width = thread_pitch - thread_tip_width - thread_tol
upper_internal_height = total_internal_height - lower_depth
flat_width = thread_maj_dia + (outer_dia - thread_maj_dia) / 2
upper_total_height = upper_internal_height + thread_depth + top_thickness + thread_tol

# Ugly trig for figuring out keyring geom, probably not the most efficient way to do this
phi = keyring_angle / 2
theta = 90 - phi
r = keyring_outer_dia / 2
l1 = r * sin(radians(phi))
h1 = r * cos(radians(phi))
l2 = h1 * tan(radians(theta))
l = keyring_center_dist + l1 + l2
h = l / tan(radians(theta))
keyring_pts = [(0, h), (l, 0), (0, -h)]

_lower_thread = Thread(
    apex_radius=thread_maj_dia / 2 - thread_tol,
    apex_width=thread_tip_width,
    root_radius=thread_min_dia / 2 - thread_tol,
    root_width=thread_root_width,
    pitch=thread_pitch,
    length=thread_depth,
    end_finishes=("fade", "fade"),
)
_upper_thread = Rotation(0, 0, thread_compliment_rotation) * Thread(
    apex_radius=thread_min_dia / 2 + thread_tol,
    apex_width=thread_tip_width,
    root_radius=thread_maj_dia / 2 + thread_tol,
    root_width=thread_root_width,
    pitch=thread_pitch,
    length=thread_depth,
    end_finishes=("fade", "fade"),
)

#finger_indents = True
def build(finger_indents: bool = True):
    with BuildPart() as _lower_base:
        Cylinder(
            thread_min_dia / 2,
            thread_depth - thread_tol,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        Cylinder(
            outer_dia / 2,
            lower_unthreaded_height,
            align=(Align.CENTER, Align.CENTER, Align.MAX),
        )
        bottom_face = _lower_base.faces().sort_by(Axis.Z)[0]
        bottom_edge = bottom_face.edges()
        chamfer(bottom_edge, end_chamfer)
        top_face = _lower_base.faces().sort_by(Axis.Z, reverse=True)[0]
        with BuildSketch(top_face) as flat_sketch:
            RegularPolygon(
                side_count=8,
                rotation=360 / 8 / 2,
                radius=flat_width / 2,
                major_radius=False,
            )
        extrude(amount=-lower_total_height, mode=Mode.INTERSECT)
        lower_side_face = _lower_base.faces().sort_by(Axis.Y)[0]

    with BuildPart() as _upper_base:
        with BuildSketch(Plane.XY) as thread_outer_sketch:
            Circle(radius=outer_dia / 2)
            Circle(radius=thread_maj_dia / 2 + thread_tol, mode=Mode.SUBTRACT)
        extrude(amount=thread_depth + thread_tol)
        top_face = _upper_base.faces().sort_by(Axis.Z, reverse=True)[0]
        with BuildSketch(top_face):
            Circle(radius=outer_dia / 2)
            Circle(radius=thread_min_dia / 2, mode=Mode.SUBTRACT)
        extrude(amount=upper_internal_height)
        inner_edge = (
            _upper_base.edges(select=Select.LAST)
            .filter_by(GeomType.CIRCLE)
            .sort_by(SortBy.RADIUS)[:2]
            .sort_by(Axis.Z)[0]
        )
        # chamfer_len1 = _upper.part.max_fillet([inner_edge], max_iterations=100)
        chamfer_len1 = 0.8185003700884692
        chamfer(
            objects=inner_edge,
            length=upper_inner_chamfer_length,
            length2=chamfer_len1,
        )
        top_face = _upper_base.faces().sort_by(Axis.Z, reverse=True)[0]
        with BuildSketch(top_face):
            Circle(radius=outer_dia / 2)
        extrude(amount=top_thickness)

        top_face = _upper_base.faces().sort_by(Axis.Z, reverse=True)[0]
        chamfer(top_face.edges(), end_chamfer)

        with BuildSketch(top_face) as flat_sketch:
            RegularPolygon(
                side_count=8,
                rotation=360 / 8 / 2,
                radius=flat_width / 2,
                major_radius=False,
            )
        extrude(amount=-upper_total_height, mode=Mode.INTERSECT)
        upper_side_face = _upper_base.faces().sort_by(Axis.Y)[0]


    if finger_indents:
        with BuildPart() as _finger_indent_tool:
            with BuildSketch(Plane.XZ) as _finger_indent_sketch:
                add(upper_side_face)
                add(lower_side_face)
                offset(amount=-finger_indent_margin)
            #extrude(amount=1)  # Attempt to fix broken step export (doesn't seem to work)
            bbox = Compound([_finger_indent_sketch.sketch]).bounding_box()
            bbox_w, _, bbox_h = bbox.max - bbox.min
            center_z = bbox.min.Z + bbox_h / 2
            center_point = Vector(0, finger_indent_depth, center_z)

            tangent_plane = Plane.XZ.offset(finger_indent_depth)
            sketch_wire = _finger_indent_sketch.sketch.wire()
            assert sketch_wire is not None
            sketch_edges = _finger_indent_sketch.sketch.edges().sort_by(sketch_wire)
            sketch_points = _finger_indent_sketch.sketch.vertices().sort_by(sketch_wire)
            sketch_points1 = sketch_points[: len(sketch_points) // 2]
            sketch_points2 = sketch_points[len(sketch_points) // 2 :]
            sketch_edges1 = sketch_edges[: len(sketch_edges) // 2]
            sketch_edges2 = sketch_edges[len(sketch_edges) // 2 :]
            if len(sketch_points1) != len(sketch_points2):
                raise ValueError("Expected an even number of points for finger indent")
            faces = ShapeList()
            for idx in range(len(sketch_points1)):
                p1 = sketch_points1[idx].center()
                p2 = sketch_points2[idx].center()
                try:
                    p1n = sketch_points1[idx + 1].center()
                    p2n = sketch_points2[idx + 1].center()
                except IndexError:
                    p1n = sketch_points2[0].center()
                    p2n = sketch_points1[0].center()

                _cross_arc = ThreePointArc(p1, center_point, p2, mode=Mode.PRIVATE)
                _cross_arc_n = ThreePointArc(p1n, center_point, p2n, mode=Mode.PRIVATE)
                with BuildLine() as finger_indent_lines1:
                    wire1 = add(sketch_edges1[idx])
                    arc1 = TangentArc([p1, center_point], tangent=_cross_arc % 0)
                    arc1n = TangentArc([p1n, center_point], tangent=_cross_arc_n % 0)
                faces.append(Face.make_surface(finger_indent_lines1.wire()))
                with BuildLine() as finger_indent_lines2:
                    wire2 = add(sketch_edges2[idx])
                    arc2 = TangentArc([center_point, p2], tangent=_cross_arc % 0.5)
                    arc2n = TangentArc([center_point, p2n], tangent=_cross_arc_n % 0.5)
                faces.append(Face.make_surface(finger_indent_lines2.wire()))
            add(Solid(Shell(faces + ShapeList([_finger_indent_sketch.sketch]))))

        with BuildPart() as _finger_indents:
            # HACK: Extra offset is required for STEP export to not be broken
            with PolarLocations(radius=flat_width / 2 + 0.0001, count=8):
                add(_finger_indent_tool.part.rotate(Axis.Z, 90))

        with BuildPart() as _lower_finger_indents:
            add(_lower_base)
            add(_finger_indents, mode=Mode.SUBTRACT)
        _lower_base = _lower_finger_indents

        with BuildPart() as _upper_finger_indents:
            add(_upper_base)
            add(_finger_indents, mode=Mode.SUBTRACT)
        _upper_base = _upper_finger_indents

    with BuildPart() as _lower:
        add(_lower_base)
        top_face = _lower.faces().sort_by(Axis.Z, reverse=True)[0]
        bottom_face = _lower.faces().sort_by(Axis.Z)[0]
        with BuildSketch(bottom_face) as keyring_sketch:
            with BuildLine():
                FilletPolyline(keyring_pts, radius=keyring_outer_dia / 2, close=True)
            make_face()
            with Locations((keyring_center_dist, 0)):
                Circle(radius=keyring_inner_dia / 2, mode=Mode.SUBTRACT)
        extrude(amount=-keyring_thickness)
        with BuildSketch(top_face):
            RegularPolygon(
                side_count=8,
                rotation=360 / 8 / 2,
                radius=face_to_face_dist / 2,
                major_radius=False,
            )
        extrude(amount=-lower_depth, mode=Mode.SUBTRACT)
        with BuildSketch():
            Circle(radius=clearance_hole_dia / 2)
        extrude(amount=-lower_unthreaded_height, mode=Mode.SUBTRACT)
    lower = Compound([_lower.part, _lower_thread])
    upper = Compound([_upper_base.part, _upper_thread])
    return lower, upper

lower, upper = build(finger_indents=False)
lower_finger_indents, upper_finger_indents = build(finger_indents=True)


results = {
    "lower": lower,
    "upper": upper,
    "lower_finger_indents": lower_finger_indents,
    "upper_finger_indents": upper_finger_indents,
}

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
        )
    except ImportError:
        pass
