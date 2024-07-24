 {
  description = "A NixOS flake with GitPython and a NixOS module";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: let
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };
  in
  {
      devShells.${system}.default = pkgs.mkShell 
      {
        buildInputs = 
        [
            pkgs.cups
            pkgs.python3
            pkgs.python312Packages.flask
            pkgs.python312Packages.pillow

        ];
     };
  };
}
