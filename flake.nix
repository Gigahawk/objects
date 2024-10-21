{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix, ... }:
    flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { inherit system; };
      inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryEnv defaultPoetryOverrides;
      poetryEnv = mkPoetryEnv {
        projectDir = ./.;
        python = pkgs.python311;
        # https://github.com/nix-community/poetry2nix/blob/master/docs/edgecases.md
        overrides = defaultPoetryOverrides.extend
          (final: prev: {
            cq-warehouse = prev.cq-warehouse.overridePythonAttrs
              ( old: { buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ]; } );
            ocp-tessellate = prev.ocp-tessellate.overridePythonAttrs
              ( old: { buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ]; } );
            svgpathtools = prev.svgpathtools.overridePythonAttrs
              ( old: { buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ]; } );
            ocpsvg = prev.ocpsvg.overridePythonAttrs
              ( old: { buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ]; } );
            trianglesolver = prev.trianglesolver.overridePythonAttrs
              ( old: { buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ]; } );
            ## Not sure why just overriding build inputs doesn't work for this package
            casadi = pkgs.python311Packages.casadi;
            #casadi = prev.casadi.override {
            #  preferWheel = true;
            #  buildInputs = [ ];
            #};
            ##casadi = prev.casadi.overridePythonAttrs
            ##  ( old: {
            ##    buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ];
            ##    nativeBuildInputs = (old.nativeBuildInputs or [ ]) ++ [ prev.cmake ];
            ##  });
            cadquery = prev.cadquery.overridePythonAttrs
              ( old: { buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ]; } );
            ipykernel = pkgs.python311Packages.ipykernel;
            ocp-vscode = prev.ocp-vscode.overridePythonAttrs
              ( old: { buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ]; } );
            ipython = pkgs.python311Packages.ipython;
            typing-extensions = pkgs.python311Packages.typing-extensions;
            six = pkgs.python311Packages.six;
          });
      };
    in {
      devShells.default = pkgs.mkShell {
        buildInputs = [
          poetryEnv
          pkgs.fontconfig
        ];
        shellHook = ''
          # https://github.com/NixOS/nixpkgs/issues/176081#issuecomment-1145825623
          export FONTCONFIG_FILE=${pkgs.fontconfig.out}/etc/fonts/fonts.conf
          export FONTCONFIG_PATH=${pkgs.fontconfig.out}/etc/fonts/
        '';
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