"""Deck box for Star Realms (with sleeves)"""

from build123d import *

card_tol = 0.1

_card_width = 66.7
card_width = _card_width + card_tol
card_height = 92.7
card_thickness = 62.7 / (80 + 10 + 16 + 4 + 4)

wall_thickness = 4
wall_chamfer = 1.5

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
tray_height = card_height/3
tray_depth = tray_height - 3

cover_tol = 0.1
cover_wall_thickness = 2
cover_lip_width = tray_width + 2*cover_wall_thickness + cover_tol
cover_lip_length = tray_length + 2*cover_wall_thickness + cover_tol
cover_lip_thickness = 2


with BuildPart() as tray:
    Box(
        tray_length,
        tray_width,
        tray_height,
        align=(Align.MIN, Align.MIN, Align.MAX)
    )
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
    top_surface = tray.faces().sort_by(Axis.Z, reverse=True)[0]
    bottom_surface = tray.faces().sort_by(Axis.Z)[0]
    chamfer(top_surface.edges(), length=wall_chamfer)
    with BuildSketch(bottom_surface):
        Rectangle(cover_lip_length, cover_lip_width)
        Rectangle(tray_length, tray_width, mode=Mode.SUBTRACT)
    extrude(amount=-cover_lip_thickness)


result = tray.part

if __name__ == "__main__":
    try:
        from ocp_vscode import *
        show_all(reset_camera=Camera.KEEP)
    except ImportError:
        pass

