# Objects

CadQuery scripts for physical objects.

## Requirements

- Install [nix](https://nixos.org/download/) and [enable flakes](https://nixos.wiki/wiki/flakes)

## Usage

### Development

- Run `nix develop` to activate the dev environment
    - The first run will involve compiling This involves compiling VTK from scratch, this will take a while.
- Run `python -m ocp-vscode` to activate the web viewer, then navigate to http://localhost:3939/viewer

### Upgrading dependencies

- Activate the `uv` environment with `nix develop .#uv`
- Update the targeted version in `pyproject.toml`, then run `uv lock`
- `exit` the dev environment, then rebuild the dev environment with `nix develop`

### Exporting

#### Locally

Running `python export.py` will create STEP files for importing into other CAD packages as well as mesh files for 3D printing

> Use `-f part.py` to export a single file only

#### On GitHub

Every push to GitHub will kick off a build action that runs `export.py` and uploads the exported files as build artifacts.



