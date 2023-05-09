from pathlib import Path
import os
import shutil
from importlib import import_module

import cadquery as cq
from cadquery import exporters

export_types = [
    ".stl",
    ".step",
    ".amf",
]


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
                        print(f"Exporting to {export_path}")
                        exporters.export(result, str(export_path))

if __name__ == "__main__":
    main()

