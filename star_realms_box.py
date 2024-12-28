"""Deck box for Star Realms (with sleeves)"""

from build123d import *

card_tol = 0.1

_card_width = 66.7
card_width = _card_width + card_tol
card_height = 92.7
card_thickness = 62.7 / (80 + 10 + 16 + 4 + 4)

wall_thickness = 4
wall_chamfer = 1.5

corner_chamfer = 2

retaining_nub_pos_dia = 3
retaining_nub_tol = 0.2
retaining_nub_neg_dia = retaining_nub_pos_dia + retaining_nub_tol
retaining_nub_height = 6

starting_cards = 10
starting_thickness = starting_cards * card_thickness
starting_extra_space = 5

# Cards for Frontiers + Colony Wars
starting_decks = 2 + 4
explorer_cards = 10 + 16
explorer_thickness = explorer_cards * card_thickness

trade_cards = 80
trade_thickness = trade_cards * card_thickness

tray_length = (
    wall_thickness
    + trade_thickness
    + wall_thickness
    + trade_thickness
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
tray_depth = tray_height - tray_bottom_thickness

cover_tol = 0.2
cover_wall_thickness = 2
cover_lip_width = tray_width + 2*cover_wall_thickness + cover_tol
cover_lip_length = tray_length + 2*cover_wall_thickness + cover_tol
cover_lip_thickness = 2
cover_clearance = 10
cover_inner_height = card_height + tray_bottom_thickness - cover_lip_thickness + cover_clearance


with BuildPart() as tray:
    Box(
        tray_length,
        tray_width,
        tray_height,
        align=(Align.MIN, Align.MIN, Align.MAX)
    )
    corner_edges = tray.edges().filter_by(Axis.Z)
    chamfer(corner_edges, length=corner_chamfer)

    with BuildSketch() as layout:
        with Locations((wall_thickness, wall_thickness)):
            with GridLocations(x_spacing=trade_thickness + wall_thickness, y_spacing=0, y_count=1, x_count=2, align=Align.MIN):
                Rectangle(trade_thickness, card_width, align=Align.MIN)
        with Locations((wall_thickness, 2*wall_thickness + card_width)):
            with GridLocations(x_spacing=starting_thickness + wall_thickness + starting_extra_space, y_spacing=0, y_count=1, x_count=starting_decks, align=Align.MIN):
                Rectangle(starting_thickness, card_width, align=Align.MIN)
        with Locations((tray_length - wall_thickness, tray_width - wall_thickness)):
            Rectangle(explorer_thickness, card_width, align=Align.MAX)
    extrude(amount=-tray_depth, mode=Mode.SUBTRACT)
    card_surface = tray.faces(select=Select.LAST).filter_by(Axis.Z).sort_by(Axis.Z)[0]
    top_surface = tray.faces().sort_by(Axis.Z, reverse=True)[0]
    bottom_surface = tray.faces().sort_by(Axis.Z)[0]
    chamfer(top_surface.edges(), length=wall_chamfer)
    with BuildSketch(bottom_surface) as cover_lip_sketch:
        # Need to project to current sketch local coordinates
        _cover_project_sketch = project(bottom_surface)
        offset(_cover_project_sketch, cover_wall_thickness + cover_tol/2, kind=Kind.INTERSECTION)
    extrude(amount=-cover_lip_thickness)

    cover_lip_top_surface = tray.faces(select=Select.LAST).filter_by(Axis.Z).sort_by(Axis.Z, reverse=True)[0]

    with Locations(
        (0, tray_width/2, -tray_height + retaining_nub_height),
        (tray_length, tray_width/2, -tray_height + retaining_nub_height)
    ):
        Sphere(retaining_nub_neg_dia/2, mode=Mode.SUBTRACT)

with BuildPart() as _cards:
    with BuildSketch(card_surface):
        Rectangle(card_thickness, card_width)
    extrude(amount=card_height)

with BuildPart() as cover:
    with BuildSketch(cover_lip_top_surface) as cover_walls_sketch:
        _cover_project_sketch = make_face(project(bottom_surface.edges(), mode=Mode.PRIVATE))
        offset(_cover_project_sketch, cover_wall_thickness + cover_tol/2, kind=Kind.INTERSECTION)
        offset(_cover_project_sketch, cover_tol/2, kind=Kind.INTERSECTION, mode=Mode.SUBTRACT)

    extrude(amount=cover_inner_height)

    with Locations(
        (0, tray_width/2, -tray_height + retaining_nub_height),
        (tray_length, tray_width/2, -tray_height + retaining_nub_height)
    ):
        Sphere(retaining_nub_pos_dia/2)


result = tray.part

if __name__ == "__main__":
    try:
        from ocp_vscode import *
        show_all(reset_camera=Camera.KEEP)
    except ImportError:
        pass

