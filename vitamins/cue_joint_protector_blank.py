from math import tan, radians
from build123d import *

ALIGN = (Align.CENTER, Align.CENTER, Align.MIN)


class CueJointProtectorBlank(BasePartObject):
    def __init__(
        self,
        total_length: float,
        outer_dia: float,
        num_faces: int = 6,
        top_loft_chamfer_inset: float = 1.5,
        top_loft_chamfer_angle: float = 60,
        top_secondary_chamfer_len: float = 1,
        notch_start: float = 4,
        notch_height: float = 1,
        notch_depth: float = 0.8,
        notch_count: int = 3,
        notch_offset: float = 2.5,
        protection_ring_thickness: float = 1.25,
        protection_ring_height: float = 6,
        protection_ring_upper_chamfer_len: float = 2,
        # HACK: To compensate for loft cut
        protection_ring_extra: float = 0.2,
        **kwargs,
    ):
        self.outer_dia = outer_dia
        self.top_loft_chamfer_inset = top_loft_chamfer_inset
        self.top_loft_chamfer_angle = top_loft_chamfer_angle
        self.total_length = total_length
        self.protection_ring_thickness = protection_ring_thickness

        with BuildPart() as protector_blank:
            # Main body
            with BuildSketch():
                Circle(outer_dia / 2)
            extrude(amount=total_length)

            top_face = faces().sort_by(Axis.Z)[-1]
            bot_face = faces().sort_by(Axis.Z)[0]

            # Cut flat sides
            with BuildSketch(top_face) as loft_top:
                RegularPolygon(
                    side_count=num_faces,
                    radius=outer_dia / 2,
                    major_radius=True,
                )
            with BuildSketch(bot_face) as loft_bot:
                RegularPolygon(
                    side_count=num_faces,
                    radius=outer_dia / 2,
                    major_radius=False,
                )
            loft(sections=[loft_top.sketch, loft_bot.sketch], mode=Mode.INTERSECT)

            # Cut primary top chamfer
            with BuildSketch(top_face) as chamfer_loft_top:
                RegularPolygon(
                    side_count=num_faces,
                    radius=self.top_chamfer_loft_top_dia / 2,
                    major_radius=True,
                )
            with BuildSketch(bot_face) as chamfer_loft_bot:
                RegularPolygon(
                    side_count=num_faces,
                    radius=self.top_chamfer_loft_bot_dia / 2,
                    major_radius=True,
                )
            loft(
                sections=[chamfer_loft_top.sketch, chamfer_loft_bot.sketch],
                mode=Mode.INTERSECT,
            )

            # Cut secondary chamfer
            top_face = faces().sort_by(Axis.Z)[-1]
            chamfer(top_face.edges(), length=top_secondary_chamfer_len)

            # Grip notches
            with BuildSketch(Plane.XZ) as notch_sketch:
                point = Vector(outer_dia / 2, top_face.center().Z - notch_start)
                with Locations(point):
                    with GridLocations(
                        x_spacing=0,
                        y_spacing=-notch_offset,
                        x_count=1,
                        y_count=notch_count,
                        align=Align.MIN,
                    ):
                        Rectangle(
                            width=notch_depth, height=notch_height, align=Align.MAX
                        )
            revolve(axis=Axis.Z, mode=Mode.SUBTRACT)

            # Protection ring
            with BuildSketch(Plane.YZ) as protection_ring_sketch:
                with BuildLine():
                    Polyline(
                        [
                            (outer_dia / 2 - protection_ring_extra, 0),
                            (self.protection_ring_dia / 2, 0),
                            (self.protection_ring_dia / 2, protection_ring_height),
                            (
                                outer_dia / 2 - protection_ring_extra,
                                protection_ring_height,
                            ),
                        ],
                        close=True,
                    )
                make_face()
                outer_corners = protection_ring_sketch.vertices().sort_by(
                    Axis.X, reverse=True
                )[:2]
                nom_chamfer = (self.protection_ring_dia - outer_dia) / 2
                top_corner = outer_corners.sort_by(Axis.Y)[-1]
                bot_corner = outer_corners.sort_by(Axis.Y)[0]
                chamfer(bot_corner, length=nom_chamfer)
                chamfer(
                    top_corner,
                    length=protection_ring_upper_chamfer_len,
                    length2=nom_chamfer + protection_ring_extra,
                )
            revolve(axis=Axis.Z)

        super().__init__(part=protector_blank.part, **kwargs)

    @property
    def top_chamfer_loft_top_dia(self) -> float:
        return self.outer_dia - 2 * self.top_loft_chamfer_inset

    @property
    def top_chamfer_loft_bot_dia(self) -> float:
        return self.top_chamfer_loft_top_dia + 2 * (
            self.total_length / tan(radians(self.top_loft_chamfer_angle))
        )

    @property
    def protection_ring_dia(self) -> float:
        return self.outer_dia + self.protection_ring_thickness * 2


default = CueJointProtectorBlank(
    total_length=42.95,
    outer_dia=21.5,
)

if __name__ == "__main__":
    try:
        from ocp_vscode import *

        show_all(reset_camera=Camera.KEEP, render_joints=True)
    except ImportError:
        pass
