# Flow of the code

##Common functions and classes

The complete .tgff file in the E3S Benchmark represent a scenario with multiple application task graphs with `tasks` and `arcs` between the messages.

Both the files take .tgff files from the E3S benchmark as the input.
The source classes for both the files are stored in their respective `source.py` files present in the respective directories. These source files contain the class details.

The code also takes the name of the cores and the name of the task graphs as an input as to facilitate the running of the code on any pseudo-random graphs generated using the tgff software.

The `get_blocks` function processes the .tgff file and isolates each block in the file, which could be either a task graph or a processing element.
The `process_block`function takes this isolated block as input and adds the appropriate `graph` or `all_tables` to the `scenario` class.
The `graph` class is populated with the tasks and the arcs with their names and some basic arc_details.
The `populate_task_params` function is used to populate the tasks with the list of the valid processing elements and other PE specific details such as WCET, power and pre-emption time.

##LP file based solvers

Now that the `graph` i.e. the application graph is populated, we use the information in the generate and solve ILPs using ILP lp_files

### Single ILP approach

The first function is the `generate_ILP` function which is used to the generate a complete ILP. The pseudo code is as follows :

```python
def generate_ILP( PATH_of_output_file, Application_graph)

    Open file:
      write Optimization function comprising of the variables in the ILP

      #write the ILP equations to cluster the tasks
      for t1 in all_tasks:
        write(t1_master+t1_slave=1)
        for t2 in all_tasks:
          #unidirectional connect in t1 and t2 is represented by C_t1_t2 directed from t2 to t1.
          Add constraints for ensuring there is a global order between the tasks.

        ensure that a task cluster signified by t_master is connected to only 1 PE.
        Also ensure that chosen PE is connected to only the allowed PEs for the given cluster.#
        # As this is done pre-clustering, it has a lot of overhead.

        assign a dvfs level to each task cluster.

      for m in messages:
        assign a Service level
        assign a Hop level

      for variables in all_variables:
        write variables to binary variable list.
    Close file.
```

After the Solver is run, we run gurobi on the file by using command line interface of python. If things go right we get an output file of assignments. Else we throw an error.

The output file of assignments returned by gurobi needs to be read and a constraint graph must be generated. This is done by the `generate_con_graph` function
```python
  def generate_con_graph:
    Read(file):
      read the clustering information and create clusters.
      Assign Processing element type to each cluster.
      Assign service level and hop distance of each message between the clusters.
```

The above generated ILP as a lp_file can be edited using the `edit_ILP` function that adds the passed constraints and variables to any lp_file.

### Modular ILP approach.
In this approach each process of the DSE is done seperately to ensure maximum design space pruning and more freedom in changing the formulation of the ILP and hence the solution.

The first ILP formulation is for a symmetry eliminating clustering with lesser variables and constraints than the previous approach. This clustering is then solved by the processed to fill the Constraint graph much like the previous approach.

The processing is of note :
```python
  def process_clustering:
    #Processing the solution file to get clusters of tasks

    #Adding the possible PEs to each task cluster
    #This also reduces the DSE as now we only need to Map a smaller set of PES to a single cluster. This saves us O(n^2) constraints and O(n) variables on an average.

    #Additional check for making sure we do not exceed the hyperperiod by clustering too many tasks on one property

    #Ignore the messages between the same the tasks in the same cluster, this also reduces the design space.

    #add additional constraints if the conditions of feasibility are not satisfied
    #re run the ILP solver and cluster processing if necessary
```
Similar ILPs are generated for assigning PE types and the dvfs levels to the task clusters and the tasks respectively.

### MOEA Scope

The above approach is currently implemented standalone.
By using a combination of generating random solution using random optimization functions for the ILP solver, changing the optimization functions and adding additional constraints we can instantiate a population and implement mutate and cross-over operations. This could have practical value although theoritically unsound.

##DPLL based solvers

The rationale behind implementing a DPLL based solver is to expose the solving methodology in the form of a decision strategy. This decision strategy can enable us to direct the solution of the ILP in a particular direction.

The key components of the DPLL solver are similar to the lp file based approach explained above.

The ILP generation function generates a dictionary with the list of the constraints and another dictionary with the variable values and the decision strategy instead of writing the output to the files.

The `decision_strat` associated with each element of the `Constraint_graph` class is a dictionary with each key being the `variable` and the value being the priority of assignment of each variable and the default value of the variable.

The dpll solver works as follows:
```python
  def(dpll_solver):
    for con in constraints:
      remove constraints of type "=" or "<=" with value=0
        remove all the variables in cons
          remove all the above variables from constraints

    pick topmost var from remaining variables

    delete empty feasible constraints
    return false if infeasible constraints
    if all constraints satisfied and all variables assigned:
      return true
    else:
        assign value to var:
          remove var from all constraints
          run dpll_solver on remaining variables and constraints
          if true:
            return true
        assign not of value to var:
          remove var from all constraints
          run dpll_solver on remaining variables and constraints
          if true:
            return true

    return false
```
Currently the dpll solver is not working as well as expected and hence will require some more work.

The solution can varied by the mutate operation as such:
```python
  def mutate(individual):
    for all variables in constraint graph:
      flip decision bit with probability of mutation
      increase priority of decision bit so it is assigned with more certainty
```
The cross over operation will simply be crossing over the bits of the decision values

####Evaluate function

The evaluate function is independent of the ILP solver implementation

Currently implemented evaluate function for evaluating the energy and the execution time of the given constraint graph.

The energy of implementation can be found by adding the energy of execution of each task on the allocated PE type along with the additional energy cost of communication.

For the execution time, a priority based approach can be used.
The priority of a task is determined by its precedence constraints. The lower priority task is always preceded by a higher priority task. This priority consideration aids us in ensuring the high priority task always executes before the low priority task.

Now in a cluster, the priority of the task can also aid in deciding the execution time. The higher priority task sets a lower bound on the start of execution time of the lower priority task. Hence now for a low priority task, the lower bound on execution time is set as max((execution time of all high priority tasks on cluster),(execution times of all tasks that are successors of the low priority task)).
If we iterate over all tasks in the order of their priority while setting the lower bound on start of execution time of lower priority tasks, we can obtain the net execution time of each cluster and subsequently the execution time of the whole application.

An intuitive way of looking at it is considering messaging edges between tasks of the same cluster with zero latency. A low priority task on a cluster can only run after the higher priority task has executed, just like in an DAG. Hence now all we have to do is to iterate over the DAG in a breadth first manner starting from a node with no incoming edges. 
