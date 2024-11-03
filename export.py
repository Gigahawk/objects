import click
from pathlib import Path
import os
import shutil
from importlib import import_module

import cadquery as cq
from cadquery import exporters
from build123d import Mesher


export_types = [
    ".stl",
    ".step",
    ".3mf",
    ".brep",
]

# Monkeypatch Mesher.add_shape to not throw errors
import warnings
import copy
import uuid
from typing import Iterable, Union
from build123d.build_enums import MeshType
from build123d.topology import Shape, Compound
from py_lib3mf import Lib3MF
def add_shape(
        self,
        shape: Union[Shape, Iterable[Shape]],
        linear_deflection: float = 0.001,
        angular_deflection: float = 0.1,
        mesh_type: MeshType = MeshType.MODEL,
        part_number: str = None,
        uuid_value: uuid = None,
    ):
        """add_shape

        Add a shape to the 3MF/STL file.

        Args:
            shape (Union[Shape, Iterable[Shape]]): build123d object
            linear_deflection (float, optional): mesh control for edges. Defaults to 0.001.
            angular_deflection (float, optional): mesh control for non-planar surfaces.
                Defaults to 0.1.
            mesh_type (MeshType, optional): 3D printing use of mesh. Defaults to MeshType.MODEL.
            part_number (str, optional): part #. Defaults to None.
            uuid_value (uuid, optional): value from uuid package. Defaults to None.

        Rasises:
            Warning: 3mf mesh is invalid
            Warning: Degenerate shape skipped
            Warning: 3mf mesh is not manifold
        """
        shapes = []
        for input_shape in shape if isinstance(shape, Iterable) else [shape]:
            if isinstance(input_shape, Compound):
                shapes.extend(list(input_shape))
            else:
                shapes.append(input_shape)

        for b3d_shape in shapes:
            # Create a 3MF mesh object
            mesh_3mf: Lib3MF.MeshObject = self.model.AddMeshObject()

            # Mesh the shape
            ocp_mesh_vertices, triangles = Mesher._mesh_shape(
                copy.deepcopy(b3d_shape),
                linear_deflection,
                angular_deflection,
            )

            # Skip invalid meshes
            if len(ocp_mesh_vertices) < 3 or not triangles:
                warnings.warn(f"Degenerate shape {b3d_shape} - skipped")
                continue

            # Create 3mf mesh inputs
            vertices_3mf, triangles_3mf = Mesher._create_3mf_mesh(
                ocp_mesh_vertices, triangles
            )

            # Build the mesh
            mesh_3mf.SetGeometry(vertices_3mf, triangles_3mf)

            # Add the mesh properties
            mesh_3mf.SetType(Mesher._map_b3d_mesh_type_3mf[mesh_type])
            if b3d_shape.label:
                mesh_3mf.SetName(b3d_shape.label)
            if part_number:
                mesh_3mf.SetPartNumber(part_number)
            if uuid_value:
                mesh_3mf.SetUUID(str(uuid_value))
            # mesh_3mf.SetAttachmentAsThumbnail
            # mesh_3mf.SetPackagePart

            # Add color
            self._add_color(b3d_shape, mesh_3mf)

            # Check mesh
            if not mesh_3mf.IsValid():
                #raise RuntimeError("3mf mesh is invalid")
                warnings.warn("3mf mesh is invalid")
            if not mesh_3mf.IsManifoldAndOriented():
                warnings.warn("3mf mesh is not manifold")

            # Add mesh to model
            self.meshes.append(mesh_3mf)
            self.model.AddBuildItem(mesh_3mf, self.wrapper.GetIdentityTransform())

            # Not sure is this is required...
            components = self.model.AddComponentsObject()
            components.AddComponent(mesh_3mf, self.wrapper.GetIdentityTransform())
Mesher.add_shape = add_shape

def export_build123d(result, path):
    export_type = path.suffix
    path = str(path)
    if export_type == ".step":
        result.export_step(path)
    elif export_type == ".brep":
        result.export_brep(path)
    elif export_type in [".stl", ".3mf"]:
        exporter = Mesher()
        exporter.add_shape(result)
        exporter.write(path)
    else:
        print(
            f"Error: {result} doesn't have an exporter for {export_type}")

def export_cadquery(result, path):
    if path.suffix == ".brep":
        print("Warning: no CadQuery exporter for brep format")
        return
    exporters.export(result, str(path))



@click.command()
@click.option("-f", "--file", "files", multiple=True)
def main(files):
    print("Cleaning export folder")
    if files:
        files = [Path(f) for f in files]
    else:
        files = Path(".").glob("**/*.py")
    try:
        shutil.rmtree("export")
    except FileNotFoundError:
        pass
    os.makedirs("export")
    for path in files:
        if (
            path.suffix != ".py"
            or path.stem == "export"
            or str(path).startswith(".")
        ):
            continue
        module = ".".join(path.with_suffix("").parts)
        print(f"Importing {module}")
        mod = import_module(module)
        if hasattr(mod, 'result'):
            results = {"default": mod.result}
        elif hasattr(mod, 'results'):
            results = mod.results
        else:
            print(
                f"Warning: Module {module} doesn't contain any results")
            continue

        for name, result in results.items():
            for t in export_types:
                export_path = (
                    Path("export") / (
                        path
                        .with_stem(path.stem + f"-{name}")
                        .with_suffix(t)
                    )
                )
                if isinstance(result, cq.Assembly):
                    result = result.toCompound()
                # Ensure export dir exists prior to writing to it
                export_dir = export_path.parent
                os.makedirs(export_dir, exist_ok=True)
                if "cadquery" in str(type(result)):
                    print(f"Exporting CadQuery part to {export_path}")
                    export_cadquery(result, export_path)
                else:
                    print(f"Exporting build123d part to {export_path}")
                    export_build123d(result, export_path)

if __name__ == "__main__":
    main()

