import copy
from math import tan, radians

from build123d import *

from vitamins import screw_socket_m2_5_40 as screw
from vitamins import nut_m2_5_square as nut
from vitamins.cue_joint_protector_female import (
    get_section_height,
    get_section_dia,
    THREAD_CLASSES,
)

from vitamins.cue_joint_protector_blank import CueJointProtectorBlank, ALIGN


def build(
    stem_dia: float,
    stem_extra_len: float = 0,
    tip_dia: float | None = None,
    pocket_wall_thickness: float = 4,
    pocket_depth: float = 4,
    screw_head_extra: float = 0.2,
    screw_rad_tol: float = 0.175,
    screw_tip_tol: float = 0.5,
    nut_overengagement: float = 3,
    nut_width_tol: float = 0.225,
    nut_thickness_tol: float = 0.2,
    thread_sections: list[BasePartObject] = [],
    **kwargs,
) -> Compound:
    with BuildPart() as _male:
        blank = CueJointProtectorBlank(rotation=(180, 0, 0), **kwargs)
        pocket_rad = blank.outer_dia / 2 - pocket_wall_thickness

        mating_face = faces().filter_by(Axis.Z).sort_by(Axis.Z)[-1]

        with BuildSketch(mating_face) as pocket_sketch:
            Circle(pocket_rad)
        extrude(amount=-pocket_depth, mode=Mode.SUBTRACT)

        pocket_face = faces(select=Select.LAST).filter_by(Axis.Z).sort_by(Axis.Z)[0]
        with BuildSketch(pocket_face) as stem_sketch:
            Circle(stem_dia / 2)
        extrude(amount=pocket_depth + stem_extra_len)

        section_height = stem_extra_len
        section_height_map = {}
        for section in thread_sections:
            section_height_map[section] = section_height
            height = get_section_height(section)
            dia = get_section_dia(section)
            if isinstance(section, THREAD_CLASSES):
                with Locations((0, 0, section_height)):
                    Cylinder(dia / 2, height, align=ALIGN)
            else:
                with Locations((0, 0, section_height)):
                    add(section)
            section_height += height
        if tip_dia is None:
            tip_dia = dia

        screw_head_face = faces().filter_by(Axis.Z).sort_by(Axis.Z)[-1]
        screw_head_loc = screw_head_face.center()
        screw_head_height = screw_head_loc.Z

        with BuildSketch(screw_head_face) as tip_sketch:
            Circle(tip_dia / 2)
            Circle(screw.head_radius + screw_rad_tol, mode=Mode.SUBTRACT)
        extrude(amount=screw.head_height + screw_head_extra)

        tip_face = faces().filter_by(Axis.Z).sort_by(Axis.Z)[-1]
        tip_edge = (
            tip_face.edges()
            .filter_by(GeomType.CIRCLE)
            .sort_by(lambda x: x.radius, reverse=True)[0]
        )
        tip_fillet = _male.part.max_fillet([tip_edge], max_iterations=100)
        fillet(objects=tip_edge, radius=tip_fillet)

        with BuildSketch(screw_head_face) as shank_sketch:
            Circle(screw.shank_radius)
        extrude(amount=-(screw.length + screw_tip_tol), mode=Mode.SUBTRACT)

        nut_loc = Location(
            (0, 0, screw_head_height - screw.length + nut_overengagement)
        )
        with Locations(nut_loc):
            add(
                nut.build_cutout(bridge_helper_hole_dia=screw.shank_radius * 2),
                mode=Mode.SUBTRACT,
            )

    male = Compound(
        [_male.part]
        + [
            s.moved(Location((0, 0, section_height_map[s])))
            for s in thread_sections
            if isinstance(s, THREAD_CLASSES)
        ]
    )
    RigidJoint(label="nut", to_part=male, joint_location=nut_loc)
    RigidJoint(
        label="screw",
        to_part=male,
        joint_location=Location(screw_head_loc, orientation=Vector(180, 0, 0)),
    )
    return male


default = build(
    stem_dia=4,
    stem_extra_len=10,
    total_length=42.95,
    outer_dia=21.5,
    thread_sections=[Cylinder(3, 10, align=ALIGN)],
)
_nut = copy.copy(nut.out)
_screw = copy.copy(screw.out)
default.joints["nut"].connect_to(_nut.joints["bottom"])
default.joints["screw"].connect_to(_screw.joints["head_bottom"])

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(reset_camera=Camera.KEEP, render_joints=True)
    except ImportError:
        pass
