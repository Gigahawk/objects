from math import tan, radians
from build123d import *

hinge_dia = 10
hinge_width = 50
hinge_internal_sections = 3
hinge_end_width = 5
cone_angle = 40
cone_depth = 3
hinge_gap = 0.3

cone_tip_dia = hinge_dia - 2*(cone_depth / tan(radians(cone_angle)))
hinge_length_total = (hinge_width - 2*hinge_end_width - hinge_gap)/hinge_internal_sections
hinge_length_actual = hinge_length_total - hinge_gap

assert cone_tip_dia > 0
assert hinge_length_total > 0
assert hinge_internal_sections % 2 == 1
assert cone_depth < hinge_end_width
assert hinge_gap > 0



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
                        Cylinder(
                            radius=(hinge_dia/2 + hinge_gap),
                            height=hinge_length_total + hinge_gap,
                            rotation=(0, 90, 0),
                            align=(Align.CENTER, Align.CENTER, Align.MIN)
                        )
    with BuildPart(mode=Mode.PRIVATE) as gap_cutout_child:
        Cylinder(
            radius=(hinge_dia/2), height=hinge_width,
            rotation=(0, 90, 0),
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        )
        _end_cap_cutout = Cylinder(
            radius=hinge_dia/2 + hinge_gap,
            height=hinge_end_width + hinge_gap, rotation=(0, 90, 0),
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.PRIVATE
        )
        with Locations(end_cap_locations[0]):
            add(_end_cap_cutout)
        with Locations(end_cap_locations[1]):
            with Locations((-hinge_gap, 0, 0)):
                add(_end_cap_cutout)
        
            
        for idx, l in enumerate(_internal_hinge_locations):
            if idx % 2 == 1:
                with Locations(l):
                    with Locations((hinge_end_width, 0, 0)):
                        Cylinder(
                            radius=(hinge_dia/2 + hinge_gap),
                            height=hinge_length_total + hinge_gap,
                            rotation=(0, 90, 0),
                            align=(Align.CENTER, Align.CENTER, Align.MIN)
                        )

_hinge_parts = _hinge.part.solids().sort_by(Axis.X)
hinge_parent = [p for idx, p in enumerate(_hinge_parts) if idx % 2 == 0]
hinge_child = [p for idx, p in enumerate(_hinge_parts) if idx % 2 == 1]
        

    


if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
            render_joints=True
        )
    except ImportError:
        pass
