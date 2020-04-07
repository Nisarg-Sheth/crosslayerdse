with import <pdconfig> {};

let
 python=python37;
in

stdenv.mkDerivation rec
{
  name = "yo";
  buildInputs=[python]++(with python37.pkgs; [deap graphviz]);
}
