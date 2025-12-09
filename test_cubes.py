"""An array of test cubes"""

import os
import cadquery as cq

def build(l, w, h):
    return cq.Workplane("XY").box(l, w, h)

inputs = {
    "onetwothree": {"l": 1, "w": 2, "h": 3},
    "fourfivesix": {"l": 4, "w": 5, "h": 6},
}

results = { name: build(**params) for name, params in inputs.items() }

if 'show_object' in globals():
    for name, obj in results.items():
        show_object(obj, name=name)