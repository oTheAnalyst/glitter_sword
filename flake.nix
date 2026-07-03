# flake.nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = {
    nixpkgs,
    self,
    ...
  }: let
    system = "x86_64-linux";
    #       ↑ Swap it for your system if needed
    #       "aarch64-linux" / "x86_64-darwin" / "aarch64-darwin"
    pkgs = nixpkgs.legacyPackages.${system};
  in {
    packages.${system}.dbt-duckdb = pkgs.callPackage ./dbt-duckdb.nix {};

    devShells.${system}.default = let
      pythonpkgs = (pkgs.python3.withPackages (ps:
        with ps; [
          self.packages.${system}.dbt-duckdb
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
        ])).override {ignoreCollisions = true;};
    in
      pkgs.mkShell {
        packages = with pkgs; [
          pythonpkgs
          duckdb
          dbt
          google-cloud-sdk
        ];
        shellHook = ''
          echo fish
        '';
      };
  };
}
