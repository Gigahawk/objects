from build123d import *

from vitamins import hinge 

hinge_gap = 0.2
hinge_width = 50
hinge_dia = 10

clamshell_thickness = 6.2
clamshell_length = 15


_hinge = hinge.build(
    hinge_dia=hinge_dia,
    hinge_width=hinge_width,
    hinge_gap=hinge_gap,
)

hinge_center_loc = Vector(-hinge_width/2, 0, clamshell_thickness)
clamshell_offset = Vector(0, hinge_gap/2, 0)

with BuildPart() as hinge_test_parent:
    with Locations(-clamshell_offset):
        Box(
            hinge_width, clamshell_length, clamshell_thickness,
            align=(Align.CENTER, Align.MAX, Align.MIN)
        )

    with Locations(hinge_center_loc):
        add(_hinge["parent_cutout"], mode=Mode.SUBTRACT)
        add(_hinge["parent"])

with BuildPart() as hinge_test_child:
    with Locations(clamshell_offset):
        Box(
            hinge_width, clamshell_length, clamshell_thickness,
            align=(Align.CENTER, Align.MIN, Align.MIN)
        )

    with Locations(hinge_center_loc):
        add(_hinge["child_cutout"], mode=Mode.SUBTRACT)
        add(_hinge["child"])

results = {
    "asm": Compound([hinge_test_parent.part, hinge_test_child.part])
}
        

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(
            reset_camera=Camera.KEEP,
            render_joints=True
        )
    except ImportError:
        pass
