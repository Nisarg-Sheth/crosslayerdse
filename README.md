# crosslayerdse

The repo contains all the work done on the ILP formulation and solving so far
The main directory contains the files for running things with gurobi
The directory /with_dpll contains the work on EA formulation and the implementation of the DSE using david-putnam backtracking algorithm

# The parent directory

To run the Gurobi solver on Nix-OS you can enter a nix-shell with the default.nix included in the folder by simply typing "nix-shell" in the command line.
The pre-requiste on other systems would be a compiled and installed Gurobi kit, instructions for which can be found on the gurobi website.
You also need python 3.7 with the packages "deap" and graphviz installed.
You can do that using "pip install deap" and "pip install graphviz" respectively.

Once you are in the required environment the solver can be running the complete.py file as "python complete.py"
The positional arguments of complete.py can be checked by "python complete.py -h"
The arguments that is required is the .tgff file which is taken as input by the solver.
The additional arguments can be the number of dvfs levels assigned to each processing unit.

The command "python complete.py a.tgff --dvfs 4" runs the code on the a.tgff file present in the ./with_dpll directory with 4 dvfs levels assumed.

Currently the dpll solver is broken and hence the code will run into an error.


# The ./with_dpll directory

To run the dpll solver you need to have python 3.7 with the packages "deap" and "graphviz".
You can do that using "pip install deap" and "pip install graphviz" respectively.
ALternately you can enter a nix-shell on Nix-OS by simply typing "nix-shell" on the command line of your nix system while being the folder ./with_dpll directory.

Once you are in the required environment the solver can be running the complete.py file as "python complete.py"
The positional arguments of complete.py can be checked by "python complete.py -h"
The arguments that is required is the .tgff file which is taken as input by the solver.
The additional arguments can be the number of dvfs levels assigned to each processing unit.

The command "python complete.py a.tgff --dvfs 4" runs the code on the a.tgff file present in the ./with_dpll directory with 4 dvfs levels assumed.

Currently the dpll solver is broken and hence the code will run into an error.
