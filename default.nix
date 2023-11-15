{ pkgs ? import <nixpkgs> {} }:

let
  myPython = (pkgs.python311.withPackages (ps: with ps; [colorama]));
in
pkgs.stdenv.mkDerivation rec {
  pname = "play-next";
  version = "0.1.1";

  src = ./.;

  play-next = pkgs.writeShellScriptBin "play-next" ''
    ${myPython}/bin/python ${src}/main.py
  '';

  installPhase = ''
    cp -r ${play-next} $out
  '';
}
