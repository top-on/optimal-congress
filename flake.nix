{
  description = "Flake for optimal-congress";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      poetry2nix,
    }:
    let
      lib = nixpkgs.lib;
      forAllSystems = lib.genAttrs [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
        "x86_64-darwin"
      ];
      poetryConfig = {
        projectDir = ./.;
        # when compiling locally, this flake does not work because transitive rust dependencies are not version pinned
        preferWheels = true;
      };
    in
    {
      apps = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages."${system}";
          inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
          myPythonApp = mkPoetryApplication poetryConfig;
        in
        rec {
          optimal-congress = {
            type = "app";
            program = "${myPythonApp}/bin/optimal-congress";
          };

          default = optimal-congress;
        }
      );

      formatter = forAllSystems (system: nixpkgs.legacyPackages."${system}".nixfmt-rfc-style);
    };
}
