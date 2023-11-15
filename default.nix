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

    cat > $out/bin/${pname} <<EOF
      #!${pkgs.bash}/bin/bash
      ${myPython}/bin/python ${src}/main.py
    EOF

    chmod +x $out/bin/${pname}
  '';
}
