{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";

    pyproject-nix = {
      url = "github:nix-community/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      pyproject-nix,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };

        project = pyproject-nix.lib.project.loadPyproject { projectRoot = ./.; };
        python = pkgs.python312;
      in
      {
        devShells.default =
          let
            attrs = project.renderers.withPackages {
              inherit python;
              extras = [ "tests" ];
              extraPackages = python-pkgs: [ python-pkgs.ipykernel ];
            };
            pythonEnv = python.withPackages attrs;
          in
          pkgs.mkShell {
            packages =
              [ pythonEnv ]
              ++ (with pkgs; [
                ruff
                pre-commit
              ]);
            shellHook = ''
              export PYTHONPATH="$(pwd)/src"
            '';
          };
      }
    );
}
