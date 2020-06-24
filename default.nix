with import <pdconfig> {};

let
 python=python37;
in

stdenv.mkDerivation rec
{
  name = "yo";
  buildInputs=[python gurobi9 jdk]++(with python37.pkgs; [pygmo matplotlib numpy gurobi9.gurobipy deap graphviz]);
  CLASSPATH= ".:/asf/pd.inf.tu-dresden.de/users/nish161c/tmp/Constraints/sat4j/*";
}
