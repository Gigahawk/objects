"""Stand for buffer tubes in the Arton COVID-19 test kit"""
import cadquery as cq
import string


def iterated_chars(self):
    """asdf"""
    self._iter_chars_idx = 0
    def get_char():
        text = cq.Workplane().text(
            string.ascii_uppercase[self._iter_chars_idx],
            8, 1, kind="bold",
            cut=False, combine=True,
            )
        self._iter_chars_idx += 1
        return text.val()

    return self.eachpoint(lambda loc: get_char().located(loc), True, combine=True)

cq.Workplane.iterated_chars = iterated_chars

hole_dia = 8
hole_distance = 20
holes_x = 3
holes_y = 2
hole_offset = 3.5

bulk_width = (holes_x + 0.5)*hole_distance
bulk_height = (holes_y + 0.5)*hole_distance
bulk_thickness = 15

fillet = 5
chamfer = 2.5

result = (
    cq.Workplane("XY").tag("base_plane")
    .rect(bulk_width, bulk_height, centered=True).extrude(bulk_thickness)
    .edges("|Z")
    .fillet(fillet)
    .faces(">Z").edges()
    .chamfer(chamfer)
    .faces(">Z").workplane()
    .center(0, hole_offset)
    .rarray(hole_distance, hole_distance, holes_x, holes_y, center=True)
    .hole(hole_dia)
    .faces(">Z").workplane()
    .center(0, -hole_distance/2)
    .rarray(hole_distance, hole_distance, holes_x, holes_y, center=True)
    .iterated_chars()
)