from pathlib import Path
import os
import shutil
from importlib import import_module

import cadquery as cq
from cadquery import exporters
from build123d import Unit

export_types = [
    ".stl",
    ".step",
    ".3mf",
]

def export_build123d(result, path):
    exporter_name = f"export_{path.suffix[1:]}"
    default_args = {
        "export_3mf": {
            "tolerance": 0.001,
            "angular_tolerance": 0.1,
            "unit": Unit.MM
        }
    }
    try:
        func = getattr(result, exporter_name)
        args = default_args.get(exporter_name, {})
        func(str(path), **args)
    except AttributeError:
        print(
            f"Error: {result} doesn't have an exporter called {exporter_name}")


def main():
    print("Cleaning export folder")
    try:
        shutil.rmtree("export")
    except FileNotFoundError:
        pass
    os.makedirs("export")
    for root, _, files in os.walk("."):
        for f in files:
            path = Path(root) / f
            if path.suffix == ".py" and path.stem != "export":
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
                            exporters.export(result, str(export_path))
                        else:
                            print(f"Exporting build123d part to {export_path}")
                            export_build123d(result, export_path)

if __name__ == "__main__":
    main()

