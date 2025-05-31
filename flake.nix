{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";

    flake-utils.url = "github:numtide/flake-utils";

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self, nixpkgs, flake-utils, pyproject-nix, uv2nix, pyproject-build-systems,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system:
    let
      inherit (nixpkgs) lib;
      pkgs = import nixpkgs { inherit system; };
      python = pkgs.python312;

      # cadquery-ocp needs vtk 9.3
      vtk93Deriv = import "${pkgs.path}/pkgs/development/libraries/vtk/generic.nix" {
        majorVersion = "9.3";
        minorVersion = "1";
        sourceSha256 = "sha256-g1TsCE6g0tw9I9vkJDgjxL/CcDgtDOjWWJOf1QBhyrg=";
      };
      vtk93 = (pkgs.callPackage vtk93Deriv {
        enablePython = true;
        inherit python;

        # Other stuff that callPackage doesn't fill in for some reason?
        qtdeclarative = pkgs.qt5.qtdeclarative;
        qttools = pkgs.qt5.qttools;
        qtx11extras = pkgs.qt5.qtx11extras;
        qtEnv = pkgs.qt5.qtEnv;
      }).overrideAttrs(old: {
        # cadquery-ocp wheel looks for versioned .so file names
        # TODO: figure out why this doesn't work
        #cmakeFlags = (builtins.filter (f: !(builtins.match "^-DVTK_VERSIONED_INSTALL=.*" f)) old.cmakeFlags) ++ [
        #  "-DVTK_VERSIONED_INSTALL=ON"
        #];
        cmakeFlags = old.cmakeFlags ++ [
          "-DVTK_VERSIONED_INSTALL=ON"
        ];
      });

      workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };
      overlay = workspace.mkPyprojectOverlay {
        sourcePreference = "wheel";
      };
      hacks = pkgs.callPackage pyproject-nix.build.hacks {};
      pyprojectOverrides = final: prev: {
        cadquery-ocp = prev.cadquery-ocp.overrideAttrs (old: {
          # Include vtk 9.3
          buildInputs = (old.buildInputs or [ ]) ++ [ vtk93 ];

          # TODO: this no longer happens once cadquery was included???
          # HACK: OCP imports fail with
          # `ImportError: /nix/store/5gz8cxcfjxxc5jy84cbb3pmfvhq1zcj3-cadquery-ocp-7.8.1.1.post1/lib/python3.12/site-packages/cadquery_ocp.libs/libTKIVtk-a1a167e9.so.7.8.1: undefined symbol: _ZNK9vtkObject20GetObjectDescriptionEv`
          # if vtk isn't imported first?
          #postInstall = ''
          #  main_init=$out/lib/python3.12/site-packages/OCP/__init__.py
          #  echo 'import vtk'$'\n'"$(cat $main_init)" > $main_init
          #'';
        });

        # Casadi needs a bunch of libs like libknitro.so and I have no idea where
        # they come from, just use a prebuilt from nixpkgs
        casadi = hacks.nixpkgsPrebuilt {
          from = pkgs.python3Packages.casadi;
          prev = prev.casadi;
        };

        bd-warehouse = prev.bd-warehouse.overrideAttrs
          ( old: { buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ]; } );
      };
      pythonSet =
        (pkgs.callPackage pyproject-nix.build.packages {
          inherit python;
        }).overrideScope (
          lib.composeManyExtensions [
            pyproject-build-systems.overlays.default
            overlay
            pyprojectOverrides
          ]
        );
    in {
      devShells.default =
      let
        virtualenv = pythonSet.mkVirtualEnv "objects-devenv" workspace.deps.all;
      in
      pkgs.mkShell {
        packages = [
          virtualenv
          pkgs.uv
        ];
        env = {
          UV_NO_SYNC = "1";
          UV_PYTHON = "${virtualenv}/bin/python";
          UV_PYTHON_DOWNLOADS = "never";
        };
        shellHook = ''
          # Undo dependency propagation by nixpkgs.
          unset PYTHONPATH

          # Get repository root using git. This is expanded at runtime by the editable `.pth` machinery.
          export REPO_ROOT=$(git rev-parse --show-toplevel)

          # https://github.com/NixOS/nixpkgs/issues/176081#issuecomment-1145825623
          export FONTCONFIG_FILE=${pkgs.fontconfig.out}/etc/fonts/fonts.conf
          export FONTCONFIG_PATH=${pkgs.fontconfig.out}/etc/fonts/
        '';
      };
      devShells.uv = pkgs.mkShell {
        packages = [
          pkgs.uv
          python
        ];
      };
    });
}