{ pkgs ? import <nixpkgs> {} }:

pkgs.stdenv.mkDerivation {
  pname = "play-next";
  version = "0.0.1-alpha";

  src = ./.;

  nativeBuildInputs = with pkgs; [ stack ghc ];
}
