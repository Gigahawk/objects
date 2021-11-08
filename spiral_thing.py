import cadquery as cq
from math import cos, sin, pi, sqrt

print("Defining function")

def turns(L, R, r):
    """Find number of turns in a spiral

    Args:
        L (float): height of the spiral
        R (float): radius of the spiral
        r (float): radius of the tube

    Returns:
        (float): number of turns in the spiral
    """

    return (
        2**(1/2)
        *L
        *(
            1
            /(
                (L**2*r**2 + R**4*pi**4)**(1/2)
                + R**2*pi**2
            )
        )**(1/2)
    )/2




print("Defining parameters")
radius = 10
tube_rad = 1
tube_len = 250

pitch = tube_rad*2
N = turns(tube_len, radius, tube_rad)
height = N*pitch

print("Defining path")
path = cq.Workplane(
    "XY",
    obj=cq.Wire.makeHelix(
        pitch + 0.01,
        height,
        radius
    )
)

print("Defining profile")
profile = (
    cq.Workplane(
        "XZ",
        origin=(radius, 0, 0)
    )
    .circle(tube_rad)
)

print("Defining sweep")
sweep = profile.sweep(path)

print("Final result")
result = (
    cq.Workplane("XY")
    .cylinder(10*height, radius, centered=[True, True, True])
    .cut(sweep)
)
print("Done")


