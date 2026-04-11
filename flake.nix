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
    devShells.${system}.default = pkgs.mkShell {
      packages = [
        (pkgs.python3.withPackages (python-pkgs: [
          python-pkgs.numpy
          python-pkgs.dash
          python-pkgs.pandas
          python-pkgs.duckdb
          python-pkgs.pandas
          python-pkgs.scipy
          python-pkgs.matplotlib
          python-pkgs.pyarrow
          python-pkgs.fastparquet
          python-pkgs.requests
        ]))
      ];
      buildInputs = with pkgs; [
        duckdb
      ];
    };
  };
}
