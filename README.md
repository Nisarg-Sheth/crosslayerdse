# crosslayerdse

To run a meta-heuristic on a particular tgff file. Follow the following steps.

1) Download the repository.

2) Enter `nix-shell` in a terminal opened in the parent directory. The `default.nix` contains all the pre-requisites of the framework. You need to specify the `CLASSPATH` variable as ".:`path_of_parent_directory\sat4j\*`". Alternately you can set the classpath in the terminal after running `nix-shell` as `export CLASSPATH=$CLASSPATH:path_to_parent_directory\sat4j\*`.
The prerequisites of this particular project are :-
A) Python 3.7 with the packages pygmo, matplotlib, numpy and deap installed. These packages can be installed using `pip install package_name`
B)Java Development Kit (11.0.1 and greater)
C)GNU C Compiler to compile the tgff binary

3)If the classpath is properly set, you can execute `python sat_scenario.py` and `python sat_with_meta.py` from the nix shell. The python scripts use a config file to configure the meta-heuristic.
The options of the python files are the input file in tgff format and the path of the configuration file.

A sample config file can be found the parent directory as `config.ini`. This is the default configuration file. This file explains the options of the configurations and can be modified based on the runs.

The `run_files` folder contains the bash scripts that can be used to be run the results for the whole benchmark or for a set of artificially generated graphs. The tgff binary can be compiled by going into the `tgff-3.6` folder and running `make` on the command line.

The `sat4j` folder contains a binary with a DPLL based PB solver.

The `pbsolver.java` contains code for the PB solver that reads the decision strategy and the constraints and outputs the variable assignment.

The python code generates the constraints and the saves the decision strategy in the folder specified in the config file. Then the `pbsolver.class` is used to generate a valid assignment. This assignment is used by the python code to generate the phenotype.

The repo contains all the work done on the ILP formulation and solving so far.


The following sections contain the old examples using self written PB solver and a gurobi solver.

## Refer to [EXAMPLE.md](EXAMPLE.md) for Example.

The main directory contains the files for running things with the gurobi solver.
The directory `/with_dpll` contains the work on EA formulation and the implementation of the DSE using david-putnam backtracking algorithm

## The parent directory

To run the Gurobi solver on Nix-OS you can enter a nix-shell with the default.nix included in the folder by simply typing `nix-shell` in the command line.
The pre-requiste on other systems would be a compiled and installed Gurobi kit, instructions for which can be found on the gurobi website, this is required only for the gurobi based solver.
You also need python 3.7 with the packages `deap` and graphviz installed.
You can do that using `pip install deap` and `pip install graphviz` respectively.

Once you are in the required environment the solver can be running the ILP_withdvfs.py file as `python ILP_withdvfs.py`.
The positional arguments of ILP_withdvfs.py can be checked by `python ILP_withdvfs.py -h`.
The arguments that is required is the .tgff file which is taken as input by the solver.
The additional arguments can be the number of dvfs levels assigned to each processing unit.
You can choose between either the modular solver or the complete solver by using the -m argument, Modular=1/Complete=0. The default is the complete solver.

The command `python complete.py a.tgff --dvfs 4 -m 1` runs the code on the a.tgff file present in the parent directory with 4 dvfs levels assumed and with the modular approach.

The files generated can be seen in the folder ./lp_files.
The name of the files and the directory can also be changed using the above mentioned command line arguments (-o and -d respectively).
The code also generates the application graph and the Constraint graph based on both approaches in the ./lp_files folder with appropriate names for each graph in the scenario.

To sum up,
    The output can be seen in the ./lp_files directory after running the command
    ```
    python complete.py a.tgff --dvfs 5 -m 0
    ```   

The work for integrating the gurobi solver is currently underway.

## The ./with_dpll directory

To run the dpll solver you need to have python 3.7 with the packages `deap` and `graphviz`.
You can do that using `pip install deap` and `pip install graphviz` respectively.
ALternately you can enter a nix-shell on Nix-OS by simply typing `nix-shell` on the command line of your nix system while being the folder ./with_dpll directory.

Once you are in the required environment the solver can be running the complete.py file as `python complete.py`
The positional arguments of complete.py can be checked by `python complete.py -h`
The arguments that is required is the .tgff file which is taken as input by the solver.
The additional arguments can be the number of dvfs levels assigned to each processing unit.

The command `python complete.py a.tgff --dvfs 4` runs the code on the a.tgff file present in the ./with_dpll directory with 4 dvfs levels assumed.

The code will first run to generate the constraint graph to verify the working of the dpll solver.
Then we will initialize the population for the given application graph and then run the MOEA on the same.

Currently the dpll solver is broken and hence the code will run into an error or hang or give output after a really long time for each evaluation

### Additional details about the MOEA approach

The mutate and mate function are written specifically for dpll solvers using a decision strategy OrderedDict called `decision_strat`.
The `make_individual` function is used to generate a individual or a constraint graph.
The `make_pop` is used to initialze the Population.
The `evalParams`is used to evaluate the individual for energy and execution time.
