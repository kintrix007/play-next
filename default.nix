{ pkgs ? import <nixpkgs> {} }:

let
  myPython = (pkgs.python311.withPackages (ps: with ps; [colorama]));
in
pkgs.stdenv.mkDerivation rec {
  pname = "play-next";
  version = "0.1.1";

  src = ./.;

  # Actually useful to include, because then it is available in nix-shells
  # as well.
  # Note: It is not strictly necessary to include python in buildInputs
  # for the build to succeed, since Nix will infer python being a dependency.
  buildInputs = [ myPython ];

  play-next = pkgs.writeShellScriptBin "play-next" ''
    ${myPython}/bin/python ${src}/main.py
  '';

  installPhase = ''
    cp -r ${play-next} $out
  '';
}
