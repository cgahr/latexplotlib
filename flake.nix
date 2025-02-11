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
              extraPackages =
                python-pkgs: with python-pkgs; [
                  ipykernel
                  python-lsp-server
                ];
            };
            pythonEnv = python.withPackages attrs;
          in
          pkgs.mkShell {
            packages =
              [ pythonEnv ]
              ++ (with pkgs; [
                ruff
                pre-commit
                stdenv.cc.cc.libgcc # for pre-commit ruff auto patchelf
                texliveMinimal
              ]);
            nativeBuildInputs = [ pkgs.autoPatchelfHook ];
            shellHook = ''
              patch=$(autoPatchelf ~/.cache/pre-commit/)

              export PYTHONPATH="$(pwd)/src"
            '';
          };
      }
    );
}
