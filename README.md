# crosslayerdse

The repo contains all the work done on the ILP formulation and solving so far
The main directory contains the files for running things with the gurobi solver.
The directory `/with_dpll` contains the work on EA formulation and the implementation of the DSE using david-putnam backtracking algorithm

## The parent directory

To run the Gurobi solver on Nix-OS you can enter a nix-shell with the default.nix included in the folder by simply typing `nix-shell` in the command line.
The pre-requiste on other systems would be a compiled and installed Gurobi kit, instructions for which can be found on the gurobi website.
You also need python 3.7 with the packages `deap` and graphviz installed.
You can do that using `pip install deap` and `pip install graphviz` respectively.

Once you are in the required environment the solver can be running the ILP_withdvfs.py file as `python ILP_withdvfs.py`
The positional arguments of ILP_withdvfs.py can be checked by `python ILP_withdvfs.py -h`
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

###Additional details about the MOEA approach

The mutate and mate function are written specifically for dpll solvers using a decision strategy OrderedDict called `decision_strat`.
The `make_individual` function is used to generate a individual or a constraint graph.
The `make_pop` is used to initialze the Population.
The `evalParams`is used to evaluate the individual for energy and execution time.
