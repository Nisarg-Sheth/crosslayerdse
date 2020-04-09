with import <pdconfig> {};

let
 python=python37;
in

stdenv.mkDerivation rec
{
  name = "yo";

  src = fetchFromGitHub {
    owner = "pysathq";
    repo = "pysatq";
    rev = "59e7e53df926e87e0feb04834f694c9ab1becec4";
    sha256 = "01w3i5d360a3r1g7dwc6q8knch6rvnxfw395p2cm5642hfkczk0h";
  };

  buildInputs=[python zlib]++(with python37.pkgs; [deap graphviz six]);

  buildPhase= ''
    python setup.py install
  '';
}
