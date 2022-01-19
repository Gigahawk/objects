import cadquery as cq
from math import sin, cos, pi

# Use different cylinder diameters for testing
cyl_diameters = sorted(
    [125, 100, 75, 50],
    reverse=True)

# Insulation diameter is approx 2mm
channel_diameter  = 2.5

# Thickness of each cylinder
thickness = channel_diameter*3
total_height = thickness*len(cyl_diameters)


# Distance between flats of hex bolt head
bolt_head_width = 24.5
# We need the distance between points since the release version of
# cadquery doesn't support circumscribed polygons apparently
_side_length = (bolt_head_width/2)/sin(pi/3)
_inscribed_width = _side_length*(1 + 2*cos(pi/3))

# Drive shaft dimensions
shaft_diameter = 16.5
shaft_length = 10


result = cq.Workplane("XY").tag("base_plane")

# Create cylinders
for d in cyl_diameters:
    try:
        result = result.faces(">Z").workplane()
    except ValueError:
        pass
    result = result.circle(d/2).extrude(thickness)

# Cut grooves
for i, d in enumerate(cyl_diameters):
    torus = cq.Workplane(
        obj=cq.Solid.makeTorus(
            d/2, channel_diameter/2,
            pnt=cq.Vector(0, 0, i*thickness + thickness/2)
        ))
    result = result.cut(torus, clean=True)

# Cut axle shaft
result = result.faces(">Z").workplane().hole(shaft_diameter)

# Cut hex for bolthead
result = (
    result.faces(">Z").workplane()
    .polygon(6, _inscribed_width)
    .cutBlind(shaft_length - total_height)
)

