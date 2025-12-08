from math import tan, radians
from build123d import *

#hinge_dia=10
#hinge_width=50
#hinge_internal_sections=3
#hinge_end_width=5
#hinge_cone_angle=40
#cone_depth=3
#hinge_gap=0.3
#overhang_comp=0.3

def build(
    hinge_dia=10,
    hinge_width=50,
    hinge_internal_sections=3,
    hinge_end_width=5,
    hinge_cone_angle=40,
    cone_depth=3,
    hinge_gap=0.3,
    overhang_comp=0.3,
):
    cone_tip_dia = hinge_dia - 2*(cone_depth / tan(radians(hinge_cone_angle)))
    hinge_length_total = (hinge_width - 2*hinge_end_width - hinge_gap)/hinge_internal_sections
    hinge_length_actual = hinge_length_total - hinge_gap

    assert cone_tip_dia > 0
    assert hinge_length_total > 0
    assert hinge_internal_sections % 2 == 1
    assert cone_depth < hinge_end_width
    assert hinge_gap > 0

    def get_hinge_cutout_stock(cutout_length):
        with BuildPart() as _hinge_cutout_stock:
            with BuildSketch(Plane.YZ) as hinge_cutout_profile:
                with BuildLine():
                    CenterArc(
                        center=(0, 0, 0),
                        radius=hinge_dia/2 + hinge_gap,
                        start_angle=0,
                        arc_size=180,
                    )
                    EllipticalCenterArc(
                        center=(0, 0, 0),
                        x_radius=hinge_dia/2 + hinge_gap,
                        y_radius=hinge_dia/2 + hinge_gap + overhang_comp,
                        start_angle=180,
                        end_angle=360,
                    )
                make_face()
            extrude(amount=cutout_length)
        return _hinge_cutout_stock.part

    with BuildPart() as _hinge:
        with GridLocations(
            x_spacing=hinge_width - hinge_end_width,
            y_spacing=0,
            x_count=2,
            y_count=1,
            align=(Align.MIN, Align.CENTER)
        ) as _end_cap_locations:
            Cylinder(
                radius=hinge_dia/2, height=hinge_end_width, rotation=(0, 90, 0),
                align=(Align.CENTER, Align.CENTER, Align.MIN)
            )
        end_cap_locations = list(_end_cap_locations)
        join_cone = Cone(
            bottom_radius=hinge_dia/2, top_radius=cone_tip_dia/2, height=cone_depth,
            rotation=(0, 90, 0), align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.PRIVATE
        )
        with Locations(end_cap_locations[0]):
            with Locations((hinge_end_width, 0, 0)):
                add(join_cone)
        with Locations(end_cap_locations[1]):
                add(join_cone, mode=Mode.SUBTRACT)
            
        with BuildPart(mode=Mode.PRIVATE) as _internal_hinge_section:
            Cylinder(
                radius=hinge_dia/2, height=hinge_length_actual,
                rotation=(0, 90, 0),
                align=(Align.CENTER, Align.CENTER, Align.MIN)
            )
            add(join_cone, mode=Mode.SUBTRACT)
            with Locations((hinge_length_actual, 0, 0)):
                add(join_cone)

        with GridLocations(
            x_spacing=hinge_length_total,
            y_spacing=0,
            x_count=hinge_internal_sections,
            y_count=1,
            align=(Align.MIN, Align.CENTER)
        ) as _internal_hinge_locations:
            with Locations((hinge_end_width + hinge_gap, 0, 0)):
                add(_internal_hinge_section)
        
        with BuildPart(mode=Mode.PRIVATE) as gap_cutout_parent:
            Cylinder(
                radius=(hinge_dia/2), height=hinge_width,
                rotation=(0, 90, 0),
                align=(Align.CENTER, Align.CENTER, Align.MIN)
            )
            for idx, l in enumerate(_internal_hinge_locations):
                if idx % 2 == 0:
                    with Locations(l):
                        with Locations((hinge_end_width, 0, 0)):
                            add(get_hinge_cutout_stock(hinge_length_total + hinge_gap))
        with BuildPart(mode=Mode.PRIVATE) as gap_cutout_child:
            Cylinder(
                radius=(hinge_dia/2), height=hinge_width,
                rotation=(0, 90, 0),
                align=(Align.CENTER, Align.CENTER, Align.MIN)
            )
            #_end_cap_cutout = Cylinder(
            #    radius=hinge_dia/2 + hinge_gap,
            #    height=hinge_end_width + hinge_gap, rotation=(0, 90, 0),
            #    align=(Align.CENTER, Align.CENTER, Align.MIN),
            #    mode=Mode.PRIVATE
            #)
            _end_cap_cutout = get_hinge_cutout_stock(hinge_end_width + hinge_gap)
            with Locations(end_cap_locations[0]):
                add(_end_cap_cutout)
            with Locations(end_cap_locations[1]):
                with Locations((-hinge_gap, 0, 0)):
                    add(_end_cap_cutout)
            
            for idx, l in enumerate(_internal_hinge_locations):
                if idx % 2 == 1:
                    with Locations(l):
                        with Locations((hinge_end_width, 0, 0)):
                            add(get_hinge_cutout_stock(hinge_length_total + hinge_gap))

    _hinge_parts = _hinge.part.solids().sort_by(Axis.X)
    hinge_parent = [p for idx, p in enumerate(_hinge_parts) if idx % 2 == 0]
    hinge_child = [p for idx, p in enumerate(_hinge_parts) if idx % 2 == 1]
    return {
        "parent": hinge_parent,
        "child": hinge_child,
        "parent_cutout": gap_cutout_parent,
        "child_cutout": gap_cutout_child,
    }

default = build()

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
            render_joints=True
        )
    except ImportError:
        pass
