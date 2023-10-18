"""Outer frame of the Prusa MK3

Uses the profile from 
https://github.com/prusa3d/Original-Prusa-i3/blob/MK3S/Frame/MK3v8b.dxf
"""
from build123d import *

profile = import_svg("prusa_mk3_outer_frame.svg")

l = 370
b = Box(l, l, l, align=Align.MIN)



if "show_object" in locals():
    show_object(profile)

try:
    from ocp_vscode import *
    show(profile, b)
except:
    pass