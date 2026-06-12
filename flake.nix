# flake.nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = {nixpkgs, ...}: let
    system = "x86_64-linux";
    #       ↑ Swap it for your system if needed
    #       "aarch64-linux" / "x86_64-darwin" / "aarch64-darwin"
    pkgs = nixpkgs.legacyPackages.${system};
  in {
    devShells.${system}.default = let
      pythonpkgs = ps:
        with ps; [
          numpy
          python-dotenv
          dash
          pandas
          duckdb
          pandas
          scipy
          matplotlib
          pyarrow
          fastparquet
          requests
        ];
    in
      pkgs.mkShell {
        packages = with pkgs; [
          (pkgs.python3.withPackages pythonpkgs)
          duckdb
          dbt
          google-cloud-sdk
          (quarto.override {
            extraPythonPackages = pythonpkgs;
          })
        ];
        shellHook = ''
          echo fish
        '';
      };
  };
}
