with import <nixpkgs> {};

let
 python=python37;
in

stdenv.mkDerivation rec
{
  name = "yo";

  src = fetchFromGitHub {
    owner = "pysathq";
    repo = "pysat";
    rev = "59e7e53df926e87e0feb04834f694c9ab1becec4";
    sha256 = "1f34z8qyvcz61kcvdwz40cldsl7bxrgsjil6d1j9x369xkic87ir";
  };

  buildInputs=[python zlib]++(with python37.pkgs; [deap graphviz six]);

  buildPhase= ''
    python setup.py install
  '';
}
