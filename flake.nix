{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    # https://github.com/NixOS/nixpkgs/pull/326696
    nixpkgs-casadi.url = "github:Sigmanificient/nixpkgs?ref=AeroSandbox";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs = { self, nixpkgs, nixpkgs-casadi, flake-utils, poetry2nix, ... }:
    flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { inherit system; };
      pkgs-casadi = import nixpkgs-casadi { inherit system; };
      inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryEnv defaultPoetryOverrides;
      poetryEnv = mkPoetryEnv {
        projectDir = ./.;
        # https://github.com/nix-community/poetry2nix/blob/master/docs/edgecases.md
        overrides = defaultPoetryOverrides.extend
          (final: prev: {
            cq-warehouse = prev.cq-warehouse.overridePythonAttrs
              ( old: { buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ]; } );
            trianglesolver = prev.trianglesolver.overridePythonAttrs
              ( old: { buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ]; } );
            numpy-quaternion = prev.numpy-quaternion.overridePythonAttrs
              ( old: { buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ]; } );
            # Not sure why just overriding build inputs doesn't work for this package
            casadi = pkgs-casadi.python312Packages.casadi;
            #casadi = prev.casadi.override {
            #  preferWheel = true;
            #  buildInputs = [ ];
            #};
            #casadi = prev.casadi.overridePythonAttrs
            #  ( old: {
            #    buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ];
            #    nativeBuildInputs = (old.nativeBuildInputs or [ ]) ++ [ prev.cmake ];
            #  });
            ocp-tessellate = prev.ocp-tessellate.overridePythonAttrs
              ( old: { buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ]; } );
            cadquery = prev.cadquery.overridePythonAttrs
              ( old: { buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ]; } );
            svgpathtools = prev.svgpathtools.overridePythonAttrs
              ( old: { buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ]; } );
            ocpsvg = prev.ocpsvg.overridePythonAttrs
              ( old: { buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ]; } );
          });
      };
    in {
      devShells.default = pkgs.mkShell {
        buildInputs = [
          poetryEnv
        ];
      };
      devShells.poetry = pkgs.mkShell {
        buildInputs = [
          # Required to make poetry shell work properly
          pkgs.bashInteractive
        ];
        packages = [
          pkgs.poetry
        ];
      };
    });
}