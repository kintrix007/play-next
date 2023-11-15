{ pkgs ? import <nixpkgs> {} }:

let
  myPython = (pkgs.python311.withPackages (ps: with ps; [colorama]));
in
pkgs.stdenv.mkDerivation rec {
  pname = "play-next";
  version = "0.1.1";

  src = ./.;

  installPhase = ''
    mkdir -p $out/bin

    cp ${pkgs.writeShellScriptBin "play-next" ''
      ${myPython}/bin/python ${src}/main.py
    ''}/bin/* $out/bin/

    chmod +x $out/bin/${pname}
  '';
}
