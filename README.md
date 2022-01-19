# Objects

CadQuery scripts for physical objects.

## Requirements

- Install [Anaconda](https://docs.anaconda.com/anaconda/install/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Open an Anaconda/Miniconda shell in this directory, then run `conda env create -f environment.yml` to install the conda environment

## Usage

### Development

- In an Anaconda/Miniconda shell, run `conda activate cadquery` to activate the conda environment
- Run `CQ-Editor` to visualize a part while it is still in development

### Exporting

#### Locally

Running `python export.py` will create STEP files for importing into other CAD packages as well as mesh files for 3D printing

#### On GitHub

Every push to GitHub will kick off a build action that runs `export.py` and uploads the exported files as build artifacts.



