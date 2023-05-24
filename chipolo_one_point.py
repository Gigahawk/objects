"""Dummy part matching the dimensions of a Chipolo ONE Point

https://chipolo.net/en-us/products/chipolo-one-point
"""

from build123d import *

thickness = 6.4
diameter = 37.9
keychain_diameter = 5.08
keychain_offset = 13.27
outer_fillet = 0.3
inner_fillet = 1

radius = diameter/2
keychain_radius = keychain_diameter/2



with BuildPart() as part:
    Cylinder(radius, thickness)
    fillet(
        part.edges(),
        radius=outer_fillet
    )
    with Locations((0, keychain_offset, 0)):
        Cylinder(keychain_radius, thickness, mode=Mode.SUBTRACT)
        fillet(
            part.edges(),
            radius=inner_fillet
        )

result = part.part

if "show_object" in locals():
    show_object(result)