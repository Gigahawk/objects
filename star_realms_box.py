"""Deck box for Star Realms (with sleeves)"""

from build123d import *

card_width = 66.7
card_height = 92.7
card_thickness = 62.7 / (80 + 10 + 16 + 4 + 4)

corner_chamfer = 2.5

hole_dia = 3.9
hole_distance = 59.5 + hole_dia



#result = bracket.part
#
#if __name__ == "__main__":
#    if "show_object" in locals():
#        show_object(bracket)
#
#    try:
#        from ocp_vscode import *
#        show_all()
#    except ImportError:
#        pass
#
#