"""Deck box for Star Realms (with sleeves)

Fits the Frontiers set and one base set
"""

from build123d import *

card_tol = 0.1

_card_width = 68.6
card_width = _card_width + card_tol
card_height = 92.7
card_thickness = 62.7 / (80 + 10 + 16 + 4 + 4)
card_thickness_tol = 0.5

def _deck_thickness(_cards):
    return _cards*card_thickness + card_thickness_tol

challenge_card_width = 126
challenge_card_height = 89
challenge_cards_thickness = 3

# Only including the Frontiers manual, which is a superset of the base set manual
manual_width = 138
manual_height = 87
manual_thickness = 4

wall_thickness = 4
wall_chamfer = 1.5

corner_chamfer = 2

retaining_nub_pos_dia = 3
retaining_nub_tol = 0.2
retaining_nub_neg_dia = retaining_nub_pos_dia + retaining_nub_tol
retaining_nub_height = 14

starting_cards = 10
starting_thickness = _deck_thickness(starting_cards)
starting_extra_space = 3

# Cards for Frontiers + base set
starting_decks = 2 + 4
score_cards = starting_decks*2
score_thickness = _deck_thickness(score_cards)
explorer_cards = 10 + 16
explorer_thickness = _deck_thickness(explorer_cards)

trade_cards = 80
trade_thickness = _deck_thickness(trade_cards)

tray_cards_length = (
    wall_thickness
    + trade_thickness
    + wall_thickness
    + trade_thickness
    + wall_thickness
)

tray_length = (
    tray_cards_length
    + manual_thickness
    + wall_thickness
    + challenge_cards_thickness
    + wall_thickness
)
tray_width = (
    wall_thickness
    + card_width
    + wall_thickness
    + card_width
    + wall_thickness
)
tray_height = card_height/2
tray_bottom_thickness = 3
tray_cards_depth = tray_height - tray_bottom_thickness
tray_challenge_cards_depth = challenge_card_height/2
tray_manual_depth = manual_height/2

cover_tol = 0.8
cover_chamfer_extra_tol = 0.5
cover_wall_thickness = 2
cover_lip_width = tray_width + 2*cover_wall_thickness + cover_tol
cover_lip_length = tray_length + 2*cover_wall_thickness + cover_tol
cover_lip_thickness = 2
cover_clearance = 1.5
cover_inner_height = card_height + tray_bottom_thickness - cover_lip_thickness + cover_clearance
cover_top_chamfer = 2
cover_finger_dia = 18

logo_orig_thickness = 2
logo_xy_scale = 0.5
logo_z_scale = 0.5
logo_thickness = logo_orig_thickness*logo_z_scale
logo_tol = 0.1

with BuildPart() as tray:
    Box(
        tray_length,
        tray_width,
        tray_height,
        align=(Align.MIN, Align.MIN, Align.MAX)
    )
    # Precache bottom_surface and chamfer with nominal dimensions for offsetting,
    # then actually chamfer the object with extra tolerance
    bottom_surface = tray.faces().sort_by(Axis.Z)[0]
    fake_corner_edges = bottom_surface.vertices()
    bottom_surface = bottom_surface.chamfer_2d(
        distance=corner_chamfer, distance2=corner_chamfer, vertices=fake_corner_edges
    )
    real_corner_edges = tray.edges().filter_by(Axis.Z)
    chamfer(real_corner_edges, length=corner_chamfer + cover_chamfer_extra_tol)

    with BuildSketch() as cards_layout:
        with Locations((wall_thickness, wall_thickness)):
            with GridLocations(x_spacing=trade_thickness + wall_thickness, y_spacing=0, y_count=1, x_count=2, align=Align.MIN):
                Rectangle(trade_thickness, card_width, align=Align.MIN)
        with Locations((wall_thickness, 2*wall_thickness + card_width)):
            with GridLocations(x_spacing=starting_thickness + wall_thickness + starting_extra_space, y_spacing=0, y_count=1, x_count=starting_decks, align=Align.MIN):
                Rectangle(starting_thickness, card_width, align=Align.MIN)
        with Locations((tray_cards_length - wall_thickness, tray_width - wall_thickness)):
            Rectangle(explorer_thickness, card_width, align=Align.MAX)
        with Locations((tray_cards_length - wall_thickness - explorer_thickness - wall_thickness, tray_width - wall_thickness)):
            Rectangle(score_thickness, card_width, align=Align.MAX)
    extrude(amount=-tray_cards_depth, mode=Mode.SUBTRACT)
    card_surface = tray.faces(select=Select.LAST).filter_by(Axis.Z).sort_by(Axis.Z)[0]

    with BuildSketch() as challenge_cards_layout:
        with Locations((tray_cards_length + challenge_cards_thickness/2, tray_width/2)):
            Rectangle(challenge_cards_thickness, challenge_card_width)
    extrude(amount=-tray_challenge_cards_depth, mode=Mode.SUBTRACT)
    challenge_cards_surface = tray.faces(select=Select.LAST).filter_by(Axis.Z).sort_by(Axis.Z)[0]

    with BuildSketch() as manual_layout:
        with Locations((tray_cards_length + challenge_cards_thickness + wall_thickness + manual_thickness/2, tray_width/2)):
            Rectangle(manual_thickness, manual_width)
    extrude(amount=-tray_manual_depth, mode=Mode.SUBTRACT)
    manual_surface = tray.faces(select=Select.LAST).filter_by(Axis.Z).sort_by(Axis.Z)[0]

    cover_top = tray.faces().sort_by(Axis.Z, reverse=True)[0]
    chamfer(cover_top.edges(), length=wall_chamfer)
    with BuildSketch(bottom_surface) as cover_lip_sketch:
        offset(
            bottom_surface.moved(Location(-bottom_surface.center())),
            cover_wall_thickness + cover_tol/2,
            kind=Kind.INTERSECTION
        )
    extrude(amount=-cover_lip_thickness)

    cover_lip_top_surface = tray.faces(select=Select.LAST).filter_by(Axis.Z).sort_by(Axis.Z, reverse=True)[0]

    with Locations(
        (0, tray_width/2, -tray_height + retaining_nub_height),
        (tray_length, tray_width/2, -tray_height + retaining_nub_height)
    ):
        Sphere(retaining_nub_pos_dia/2)

with BuildPart() as _cards:
    with BuildSketch(card_surface):
        Rectangle(card_thickness, card_width)
    extrude(amount=card_height)

with BuildPart() as _challenge_cards:
    with BuildSketch(challenge_cards_surface):
        Rectangle(challenge_cards_thickness, challenge_card_width)
    extrude(amount=challenge_card_height)

with BuildPart() as _manual:
    with BuildSketch(manual_surface):
        Rectangle(manual_thickness, manual_width)
    extrude(amount=manual_height)

with BuildPart() as cover:
    with BuildSketch(cover_lip_top_surface, mode=Mode.PRIVATE) as cover_walls_base_sketch:
        _cover_project_sketch = make_face(project(bottom_surface.edges(), mode=Mode.PRIVATE))
    with BuildSketch(cover_lip_top_surface, mode=Mode.PRIVATE) as cover_walls_outer_sketch:
        offset(_cover_project_sketch, cover_wall_thickness + cover_tol/2, kind=Kind.INTERSECTION)
    with BuildSketch(cover_lip_top_surface, mode=Mode.PRIVATE) as cover_walls_inner_sketch:
        offset(_cover_project_sketch, cover_tol/2, kind=Kind.INTERSECTION)
    with BuildSketch(cover_lip_top_surface) as cover_walls_sketch:
        add(cover_walls_outer_sketch)
        add(cover_walls_inner_sketch, mode=Mode.SUBTRACT)
    extrude(cover_walls_sketch.sketch, amount=cover_inner_height)
    cover_inner = cover.faces().filter_by(Axis.Z).sort_by(Axis.Z, reverse=True)[0]
    with BuildSketch(cover_inner) as cover_top_sketch:
        # If we don't move sometimes the top doesn't get added to the right place?
        add(cover_walls_outer_sketch.sketch.moved(Location(-cover_walls_outer_sketch.sketch.center())))
    extrude(amount=cover_wall_thickness)
    cover_top = cover.faces().filter_by(Axis.Z).sort_by(Axis.Z, reverse=True)[0]
    chamfer(cover_top.edges(), length=cover_top_chamfer)

    with Locations(
        Location((tray_length/2, tray_width/2, -tray_height + retaining_nub_height), (0, 90, 0)),
    ):
        Cylinder(retaining_nub_neg_dia/2, tray_length + retaining_nub_neg_dia, mode=Mode.SUBTRACT)

    with Locations(
        Location((tray_length/2, tray_width/2, -tray_height + cover_lip_thickness), (90, 0, 0)),
        Location((tray_length/2, tray_width/2, -tray_height + cover_lip_thickness), (0, 90, 0)),
    ):
        Cylinder(cover_finger_dia/2, max(tray_length, tray_width)*2, mode=Mode.SUBTRACT)

    with BuildSketch(cover_top, mode=Mode.PRIVATE) as _logo_sketch:
        offset(
            scale(
                mirror(
                    make_face(import_svg("res/star_realms_logo.svg")),
                    about=Plane.XZ
                ),
                by=logo_xy_scale
            ),
            logo_tol,
            kind=Kind.INTERSECTION
        )
    with BuildSketch(cover_top) as logo_sketch:
        center = _logo_sketch.sketch.bounding_box().center()
        add(_logo_sketch.sketch.moved(Location(-center)))
    extrude(amount=-logo_thickness, mode=Mode.SUBTRACT)

    logo_face = cover.faces(select=Select.LAST).filter_by(Axis.Z).sort_by(Axis.Z)[0]
    RigidJoint(
        label="logo_face",
        joint_location=Location(logo_face.bounding_box().center())
    )

_logo = import_step("res/star_realms_logo.step")
_logo = Solid(_logo)
_logo = scale(
    _logo,
    by=(logo_xy_scale, logo_xy_scale, logo_z_scale)
)
logo_center = _logo.bounding_box().center()
_logo = _logo.moved(Location(-logo_center))
_logo = Rot(180, 0, 0) * _logo
with BuildPart() as logo:
    add(_logo)
    logo_bottom_face = logo.faces().filter_by(Axis.Z).sort_by(Axis.Z)[0]
    RigidJoint(
        label="logo_bottom_face",
        joint_location=Location(logo_bottom_face.bounding_box().center())
    )
logo.part.color = Color("red")
cover.part.joints["logo_face"].connect_to(logo.part.joints["logo_bottom_face"])



results = {
    "tray": tray.part,
    "cover": cover.part,
    "logo": logo.part
}

if __name__ == "__main__":
    try:
        from ocp_vscode import *
        show_all(reset_camera=Camera.KEEP, render_joints=True)
    except ImportError:
        pass

