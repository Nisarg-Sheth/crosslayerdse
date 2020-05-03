import os
import sys
import re
import argparse
import random
import subprocess
import time
import matplotlib.pyplot as plt
import numpy
from graphviz import Digraph
from deap import base
from deap import creator
from deap import tools
from source import *
from copy import deepcopy
from deap.benchmarks.tools import hypervolume

scenario = None
random.seed(124)

def get_blocks(input_file):
    buf=[]
    for line in input_file:
        if line and line.strip() and line.startswith("@"):
            buf =[]
            buf.append(line.strip())
            if not line.strip().endswith("{"):
                yield buf
                buf = []
        elif line and line.strip() and line.startswith("}"):
            yield buf
        elif line and line.strip():
            buf.append(line.strip())

def process_block(block,tg,core):
    global scenario

    if tg in block[0]:
        tg_name = None
        period = None
        for line in block:
            if line.startswith("@"):
                tg_name = line.strip('@').strip('{')
                #print(tg_name)
            elif line.startswith("PERIOD"):
                period = float(line.strip(' PERIOD'))
                scenario.graphs[tg_name]=Graph(tg_name,period)
                #print(period)
                break
        for line in block:
            if line.startswith("TASK"):
                scenario.graphs[tg_name].add_task(line.strip('TASK '))
            elif line.startswith("ARC"):
                scenario.graphs[tg_name].add_arc(line.strip('ARC '))
            elif line.startswith("SOFT_DEADLINE"):
                scenario.graphs[tg_name].add_soft_deadline(line.strip('SOFT_DEADLINE '))
            elif line.startswith("HARD_DEADLINE"):
                scenario.graphs[tg_name].add_hard_deadline(line.strip('HARD_DEADLINE '))


    elif core in block[0] or "PROC" in block[0] or "CORE" in block[0]:
        #  or " 6 " in block[0] or " 14 " in block[0]
        if " 0 " in block[0] or " 3 " in block[0] :
            core_name = None
            i = 0
            core_name= block[0].strip('@').strip('{').replace(" ","")
            print(core_name)
            scenario.all_tables[core_name]=Table(core_name,block[1].strip('#'),block[2].strip('#'),block[4].strip('#'))
            for i in range(5, len(block)):
                if not block[i].startswith('#'):
                    scenario.all_tables[core_name].add_row(block[i])
    elif "HYPERPERIOD" in block[0]:
        scenario.hyperperiod= float(block[0].strip('@HYPERPERIOD '))
    elif "COMMUN_QUANT" in block[0]:
        for i in range(len(block)):
            if(i==0):
                continue
            vals=block[i].split()
            scenario.communication[vals[0]]=float(vals[1])

def assign_priorities():
    global scenario
    for graph in scenario.graphs:
        #Assigning the task priorities
        for task in scenario.graphs[graph].tasks:
            for arc in scenario.graphs[graph].arcs:
                task_to=scenario.graphs[graph].arcs[arc].task_to
                task_from=(scenario.graphs[graph].arcs[arc].task_from)
                if scenario.graphs[graph].tasks[task_to].priority<(scenario.graphs[graph].tasks[task_from].priority+1):
                    scenario.graphs[graph].tasks[task_to].priority=(scenario.graphs[graph].tasks[task_from].priority+1)

def populate_message_params():
    global scenario
    for graph in scenario.graphs:
        for arc in scenario.graphs[graph].arcs:
            type=scenario.graphs[graph].arcs[arc].type
            if type in scenario.communication.keys():
                scenario.graphs[graph].arcs[arc].quant=scenario.communication[type]

def populate_task_params():
    global scenario
    for graph in scenario.graphs:
        for task in scenario.graphs[graph].tasks:
            task_feasible=False
            scenario.graphs[graph].tasks[task].pe_list=[]
            scenario.graphs[graph].tasks[task].wcet={}
            scenario.graphs[graph].tasks[task].power={}
            scenario.graphs[graph].tasks[task].code_bits={}
            scenario.graphs[graph].tasks[task].preempt_time={}
            type_of_task=scenario.graphs[graph].tasks[task].type
            for table in scenario.tables:
                if scenario.tables[table].values[type_of_task][0]==type_of_task:
                    if int(scenario.tables[table].values[type_of_task][2])==1:
                        task_feasible=True
                        #adding the PE to the pe_list of each task
                        scenario.graphs[graph].tasks[task].pe_list.append(table)
                        #adding the WCET on the PE for each task
                        scenario.graphs[graph].tasks[task].wcet[table]=float(scenario.tables[table].values[type_of_task][3])*(1e6)
                        #adding the task_power on the PE to the task arc_details
                        scenario.graphs[graph].tasks[task].power[table]=float(scenario.tables[table].values[type_of_task][6])
                        #adding code bits to the task details
                        scenario.graphs[graph].tasks[task].code_bits[table]=float(scenario.tables[table].values[type_of_task][5])
                        #adding preemeption_time
                        scenario.graphs[graph].tasks[task].preempt_time[table]=float(scenario.tables[table].values[type_of_task][4])
            if(task_feasible==False):
                return False


    return True

def generate_noc(length,breadth):
    global scenario
    # Random Assignment of PEs
    # print("NOC Assignment is as follows\n")
    # for i in range(length):
    #     l=[]
    #     to_print=""
    #     for j in range(breadth):
    #         name=f"PE_{i}_{j}"
    #         temp=random.sample(scenario.all_tables.keys(),1)
    #         scenario.tables[name]=scenario.all_tables[temp[0]]
    #         scenario.tables[name].name=temp[0]
    #         to_print+=f"|{name} type = {temp[0]}|"
    #         l.append(temp[0])
    #     print(to_print)
    #     scenario.NOC.append(l)
    # print("____________________________________________")
    isAssigned=False
    i=0
    j=0
    while(isAssigned==False):
        for core in scenario.all_tables:
            if(i<length and j<breadth):
                name=f"PE_{i}_{j}"
                scenario.tables[name]=scenario.all_tables[core]
                scenario.tables[name].name=core
                print(core,"is assigned to",name)
                i+=1
            elif(j<(breadth-1)):
                j+=1
                i=0
                name=f"PE_{i}_{j}"
                scenario.tables[name]=scenario.all_tables[core]
                scenario.tables[name].name=core
                print(core,"is assigned to",name)
                i+=1
            else:
                isAssigned=True
                break

#The phenotype of
def gen_phenotype(individual,graph):
    global scenario
    for task in scenario.graphs[graph].tasks:
        individual.task_list[task]=Task_data(task)
    for parts in individual.assignment:
        if individual.assignment[parts]==1:
            # print(parts)
            if parts.startswith("dvfs_"):
                d=(parts[5:])
                vars=d.split("_",1)
                individual.task_list[vars[1]].dvfs_level=int(vars[0])
            else:
                ext_id = parts.find("_")
                task=parts[:ext_id]
                mapped=parts[(ext_id+1):]
                individual.task_list[task].mapped=mapped
                if mapped in individual.pe_list.keys():
                    individual.pe_list[mapped].append(task)
                else:
                    individual.pe_list[mapped]=[task]
    for pe in individual.pe_list:
        task1=None
        for task in individual.pe_list[pe]:
            task1=task
            individual.task_cluster[task1]=[]
            break
        for task in individual.pe_list[pe]:
            individual.task_to_cluster[task]=task1
            individual.task_cluster[task1].append(task)


#generate the constraint graph from the ILP
def gen_comp_con_graph(con_graph, graph):
    global scenario
    slave_list = []
    master_list = []
    map_list = []
    c_list = []
    sl_list = []
    hop_list = []
    dvfs_list = []
    for parts in con_graph.pbp_data["complete"].assignment:
        if con_graph.pbp_data["complete"].assignment[parts]==1:
            #print(parts)
            if parts.endswith("_master"):
                ext_id = parts.rfind("_")
                master_list.append(parts[:ext_id])
            elif parts.endswith("_slave"):
                ext_id = parts.rfind("_")
                slave_list.append(parts[:ext_id])
            elif parts.startswith("map_"):
                map_list.append(parts[4:])
            elif parts.startswith("C_"):
                c_list.append(parts[2:])
            elif parts.startswith("sl_"):
                sl_list.append(parts[3:])
            elif parts.startswith("hop_"):
                hop_list.append(parts[4:])
            elif parts.startswith("dvfs_"):
                dvfs_list.append(parts[5:])

    for m in master_list:
        con_graph.task_cluster[m]=Task_cluster()
        con_graph.task_cluster[m].tasks.append(m)
        con_graph.task_to_cluster[m]=m
    for c in c_list:
        tasks=c.split("_",1)
        if tasks[1] in con_graph.task_cluster:
            con_graph.task_cluster[tasks[1]].tasks.append(tasks[0])
            con_graph.task_to_cluster[tasks[0]]=tasks[1]
    for m in map_list:
        a=m.split("_",1)
        con_graph.task_cluster[a[0]].mapped_to=a[1]
    for d in dvfs_list:
        vars=d.split("_",1)
        con_graph.dvfs_level[vars[1]]=int(vars[0])
    for sl in sl_list:
        a=sl.split("_",1)
        task_from = scenario.graphs[graph].arcs[a[1]].task_from
        task_to = scenario.graphs[graph].arcs[a[1]].task_to
        if con_graph.task_to_cluster[task_to] != con_graph.task_to_cluster[task_from]:
            con_graph.messages[a[1]]=Message()
            con_graph.messages[a[1]].cluster_from=con_graph.task_to_cluster[task_from]
            con_graph.messages[a[1]].cluster_to=con_graph.task_to_cluster[task_to]
            con_graph.messages[a[1]].sl=int(a[0])

    for hop in hop_list:
        a=hop.split("_",1)
        if a[1] in con_graph.messages:
            con_graph.messages[a[1]].hop=int(a[0])

def gen_genotype(individual,graph):
    global scenario
    num_of_vars=0
    num_of_con=0
    individual.pbp_data={}
    for task in scenario.graphs[graph].tasks:
        individual.pbp_data[task]=PB_data()
        l={}
        for mapped in scenario.graphs[graph].tasks[task].pe_list:
            temp=f"{task}_{mapped}"
            num_of_vars+=1
            individual.pbp_data[task].decision_strat[temp]=[random.uniform(0,1),bool(1)]
            l[temp]=('+',1)
        num_of_con+=1
        individual.constraints.append([l,1,'='])
        if scenario.dvfs!=None and scenario.dvfs>=3:
            l={}
            for level in range(scenario.dvfs):
                temp=f"dvfs_{level}_{task}"
                num_of_vars+=1
                individual.pbp_data[task].decision_strat[temp]=[random.uniform(0,1),bool(1)]
                l[temp]=('+',1)
            num_of_con+=1
            individual.constraints.append([l,1,'='])


def plot_app_graph(graph,phase,file_name,dir):
    app_g = Digraph(comment = graph,format='png')
    for task in scenario.graphs[graph].tasks:
        app_g.node(str(task),label=task)
    for m in scenario.graphs[graph].arcs:
        app_g.node(m,label=m)
        app_g.edge(scenario.graphs[graph].arcs[m].task_from,m)
        app_g.edge(m,scenario.graphs[graph].arcs[m].task_to)
    app_g.render(f"{dir}/{file_name}_{phase}_appgraph",view=False)

def process_pbp_data(individual):
    #sort decision strat by the increasing order of decision priority
    decision_strats=OrderedDict()
    for task in scenario.graphs[individual.graph].tasks:
        for d in individual.pbp_data[task].decision_strat:
            decision_strats[d]=deepcopy(individual.pbp_data[task].decision_strat[d])

    decision_strat=OrderedDict(deepcopy(sorted(decision_strats.items() , key=lambda x : -x[1][0])))
    # for var in decision_strat:
    #     if "fp" in var:
    #         print(var)
    #list of constraint details
    con_dets={}
    #list of constraints in which the given variable exists
    var_list={}
    for var in decision_strat:
        var_list[var]=[]
        posCons={}
        var_list[var].append(posCons)
        negCons={}
        var_list[var].append(negCons)
    i=0

    for con in individual.constraints:
        con_type=con[2]
        n=con[1]
        maxsum=0
        for var in con[0]:
            #update maximum possible sum of the constraints
            maxsum+=con[0][var][1]
            if con[0][var][0]=='-':
                #update variable coefficient in constraints in which a variable is negative
                var_list[var][1][i]=con[0][var][1]
                #update the value of the constraint value to reflect the negation of the variable
                n+=con[0][var][1]
            else:
                #update variable coefficient in constraints in which a variable is positive
                var_list[var][0][i]=con[0][var][1]
        #con_dets is a list of Constraint type(<=,>=,=) the current value of sum, maximum sum the constraint equation can reach and the objective goal
        con_dets[i]=[con_type,0,maxsum,n]
        i+=1
    isAssigned, assignment= pbs_solver(decision_strat,individual.constraints,con_dets,var_list)
    # for val in decision_strat:
    #     if val in assignment:
    #         if "idct" in val:
    #             print(assignment[val])
    #             print(val)
    #     else:
    #         print("MISSED OUT ON VARS")
    if isAssigned==False:
        print("Assignment was not successful")
        print(assignment)
        print_pb_strat(con_graph)
        return None
    return assignment

def pbs_solver(decision_strat,constraints,con_dets,variables):
    cur_var = None
    var_val = None
    assignment={}
    var_list={}
    infeasible_con_list={}
    #pick the variable to assign a value using the decision_strat
    for vars in decision_strat:
        if decision_strat[vars][0]!=(-1):
            cur_var=vars
            var_val = decision_strat[cur_var][1]
            decision_strat[cur_var][0]=-1
            break
    if cur_var==None:
        return True,assignment
    #print("The current value is ",cur_var,var_val)
    #print(cur_var)
    #print(var_val)
    #variable to check if the assignment is feasible.
    isFeasible=True
    #Updating the con_dets for the given assignment
    #Iterating over the positive constraints associated with the current variable
    for i in variables[cur_var][0]:
        #update the constraints list based on the value of the current variable.
        if var_val==1:
            #make sure that it is feasible for the constraint to be assigned true or false.
            if con_dets[i][0]!='>=':
                #if current sum + coefficient>objective goal of constraint and coefficient is positive
                if (con_dets[i][1]+variables[cur_var][0][i])>con_dets[i][3]:
                    isFeasible=False
                    infeasible_con_list[i]=1
            #add value of coefficient to current sum of constraint
            con_dets[i][1]+=variables[cur_var][0][i]
        else:
            #Make sure that assigning the value does not cause conflict
            if con_dets[i][0]!='<=':
                if (con_dets[i][2]-variables[cur_var][0][i])<con_dets[i][3]:
                    isFeasible=False
                    infeasible_con_list[i]=1
            #subtract value of coefficient from maximum posible sum of constraints
            con_dets[i][2]-=variables[cur_var][0][i]
        #check for implications or conflicts caused due to this assignment in the given constraint.
        for vars in constraints[i][0]:
            if decision_strat[vars][0]!=-1:
                if con_dets[i][0]!='>=':
                   #if current sum + coefficient>objective goal of constraint and coefficient is positive
                    if constraints[i][0][vars][0]=='+' and (con_dets[i][1]+variables[vars][0][i])>con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=False:
                                isFeasible=False
                                infeasible_con_list[i]=1
                        var_list[vars]=False
                    elif constraints[i][0][vars][0]=='-' and (con_dets[i][1]+variables[vars][1][i])>con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=True:
                                isFeasible=False
                                infeasible_con_list[i]=1
                        var_list[vars]=True
                elif con_dets[i][0]!='<=':
                    #if the coefficient of vars is necessary, make sure it is true
                    if constraints[i][0][vars][0]=='+' and (con_dets[i][2]-variables[vars][0][i])<con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=False:
                                isFeasible=False
                                infeasible_con_list[i]=1
                        var_list[vars]=False
                        #print("THIS",vars)
                    #if the sign of vars is negative in the constraint, then make sure it is false.
                    elif constraints[i][0][vars][0]=='-' and (con_dets[i][2]-variables[vars][1][i])<con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=True:
                                isFeasible=False
                                infeasible_con_list[i]=1
                        var_list[vars]=True

    for i in variables[cur_var][1]:
        #update the constraints list based on the value of the current variable.
        if var_val==0:
            #make sure that it is feasible for the constraint to be assigned true or false.
            if con_dets[i][0]!='>=':
                #if current sum + coefficient>objective goal of constraint and coefficient is positive
                if (con_dets[i][1]+variables[cur_var][1][i])>con_dets[i][3]:
                    isFeasible=False
                    infeasible_con_list[i]=1
            con_dets[i][1]+=variables[cur_var][1][i]
        else:
            #Make sure that assigning the value does not cause conflict
            if con_dets[i][0]!='<=':
                if (con_dets[i][2]-variables[cur_var][1][i])<con_dets[i][3]:
                    isFeasible=False
                    infeasible_con_list[i]=1
            con_dets[i][2]-=variables[cur_var][1][i]
        #check for implications or conflicts caused due to this assignment in the given constraint.
        for vars in constraints[i][0]:
            if decision_strat[vars][0]!=-1:
                if con_dets[i][0]!='>=':
                   #if current sum + coefficient>objective goal of constraint and coefficient is positive
                    if constraints[i][0][vars][0]=='+' and (con_dets[i][1]+variables[vars][0][i])>con_dets[i][3]:
                        if vars in var_list:
                           if var_list[vars]!=False:
                               isFeasible=False
                               infeasible_con_list[i]=1
                        var_list[vars]=False
                    elif constraints[i][0][vars][0]=='-' and (con_dets[i][1]+variables[vars][1][i])>con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=True:
                                isFeasible=False
                                infeasible_con_list[i]=1
                        var_list[vars]=True
                elif con_dets[i][0]!='<=':
                    if constraints[i][0][vars][0]=='+' and (con_dets[i][2]-variables[vars][0][i])<con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=False:
                                isFeasible=False
                                infeasible_con_list[i]=1
                        var_list[vars]=False
                    elif constraints[i][0][vars][0]=='-' and (con_dets[i][2]-variables[vars][1][i])<con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=True:
                                isFeasible=False
                                infeasible_con_list[i]=1
                        var_list[vars]=True

    #Now the var_list should be updated, process the list
    #The list contains the implications of the variable assignment
    #print("The list of implications is:")
    for val in var_list:
        #print("Implication is", val, var_list[val])
        #Iterating over the positive constraints associated with the current variable
        decision_strat[val][0]=(-1)
        for i in variables[val][0]:
            #update the constraints list based on the value of the current variable.
            if var_list[val]==1:
                #make sure that it is feasible for the constraint to be assigned true or false.
                if con_dets[i][0]!='>=':
                    #if current sum + coefficient>objective goal of constraint and coefficient is positive
                    if (con_dets[i][1]+variables[val][0][i])>con_dets[i][3]:
                                isFeasible=False
                                infeasible_con_list[i]=1
                #add value of coefficient to current sum of constraint
                con_dets[i][1]+=variables[val][0][i]
            else:
                #subtract value of coefficient from maximum posible sum of constraints
                #Make sure that assigning the value does not cause conflict
                if con_dets[i][0]!='<=':
                    if (con_dets[i][2]-variables[val][0][i])<con_dets[i][3]:
                                isFeasible=False
                                infeasible_con_list[i]=1
                con_dets[i][2]-=variables[val][0][i]
        #Iterating over the negative constraints associated with the current variable
        for i in variables[val][1]:
            #update the constraints list based on the value of the current variable.
            if var_list[val]==0:
                #make sure that it is feasible for the constraint to be assigned true or false.
                if con_dets[i][0]!='>=':
                    #if current sum + coefficient>objective goal of constraint and coefficient is positive
                    if (con_dets[i][1]+variables[val][1][i])>con_dets[i][3]:
                                isFeasible=False
                                infeasible_con_list[i]=1
                #add value of coefficient to current sum of constraint
                con_dets[i][1]+=variables[val][1][i]
            else:

                #Make sure that assigning the value does not cause conflict
                if con_dets[i][0]!='<=':
                    if (con_dets[i][2]-variables[val][1][i])<con_dets[i][3]:
                                isFeasible=False
                                infeasible_con_list[i]=1
                #subtract value of coefficient from maximum posible sum of constraints
                con_dets[i][2]-=variables[val][1][i]

    #after assigning the values of the assignment, lets check if the whole situation is feasible.
    reprocess=False
    val_return=infeasible_con_list
    if isFeasible==True:
        #print("____NEXT LEVEL___")
        isAssigned, vals= pbs_solver(decision_strat,constraints,con_dets,variables)
        if isAssigned:
            vals[cur_var]=var_val
            for val in var_list:
                vals[val]=var_list[val]
            return True, vals
        else:
            #print("recursed back to find source of infeasibility")
            reprocess=True
            val_return=vals
            for i in vals:
                infeasible_con_list[i]=1
            for i in variables[cur_var][0]:
                if i in val_return.keys():
                    reprocess=False
            for i in variables[cur_var][1]:
                if i in val_return.keys():
                    reprocess=False
            for varrs in var_list:
                for i in variables[varrs][0]:
                    if i in val_return.keys():
                        reprocess=False
                for i in variables[varrs][1]:
                    if i in val_return.keys():
                        reprocess=False

    #reset the values of con_dets to what they were before assignment and the implication
    for i in variables[cur_var][0]:
        if var_val==1:
            con_dets[i][1]-=variables[cur_var][0][i]
        else:
            con_dets[i][2]+=variables[cur_var][0][i]
    for i in variables[cur_var][1]:
        if var_val==0:
            con_dets[i][1]-=variables[cur_var][1][i]
        else:
            con_dets[i][2]+=variables[cur_var][1][i]
    for val in var_list:
        #revert the decision strategy.
        decision_strat[val][0]=1
        for i in variables[val][0]:
            if var_list[val]==1:
                con_dets[i][1]-=variables[val][0][i]
            else:
                con_dets[i][2]+=variables[val][0][i]
        for i in variables[val][1]:
            if var_list[val]==0:
                con_dets[i][1]-=variables[val][1][i]
            else:
                con_dets[i][2]+=variables[val][1][i]
    #clear var_list
    var_list={}
    if reprocess==True:
        #print(cur_var,"isn't source of infeasibility")
        decision_strat[cur_var][0]=1
        return False,val_return

    #Change the value if it is infeasible, repeat.
    var_val=not var_val
    #print(f"Swap decision variable for {cur_var}")
    # print("The current value is ",cur_var,var_val)


    #variable to check if the assignment is feasible.
    isFeasible=True
    #Updating the con_dets for the given assignment
    #Iterating over the positive constraints associated with the current variable
    for i in variables[cur_var][0]:
        #update the constraints list based on the value of the current variable.
        if var_val==1:
            #make sure that it is feasible for the constraint to be assigned true or false.
            if con_dets[i][0]!='>=':
                #if current sum + coefficient>objective goal of constraint and coefficient is positive
                if (con_dets[i][1]+variables[cur_var][0][i])>con_dets[i][3]:
                    isFeasible=False
                    infeasible_con_list[i]=1
            #add value of coefficient to current sum of constraint
            con_dets[i][1]+=variables[cur_var][0][i]
        else:
            #Make sure that assigning the value does not cause conflict
            if con_dets[i][0]!='<=':
                if (con_dets[i][2]-variables[cur_var][0][i])<con_dets[i][3]:
                    isFeasible=False
                    infeasible_con_list[i]=1
            #subtract value of coefficient from maximum posible sum of constraints
            con_dets[i][2]-=variables[cur_var][0][i]
        #check for implications or conflicts caused due to this assignment in the given constraint.
        for vars in constraints[i][0]:
            if decision_strat[vars][0]!=-1:
                if con_dets[i][0]!='>=':
                   #if current sum + coefficient>objective goal of constraint and coefficient is positive
                    if constraints[i][0][vars][0]=='+' and (con_dets[i][1]+variables[vars][0][i])>con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=False:
                                isFeasible=False
                                infeasible_con_list[i]=1
                        var_list[vars]=False
                    elif constraints[i][0][vars][0]=='-' and (con_dets[i][1]+variables[vars][1][i])>con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=True:
                                isFeasible=False
                                infeasible_con_list[i]=1
                        var_list[vars]=True
                elif con_dets[i][0]!='<=':
                    #if the coefficient of vars is necessary, make sure it is true
                    if constraints[i][0][vars][0]=='+' and (con_dets[i][2]-variables[vars][0][i])<con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=False:
                                isFeasible=False
                                infeasible_con_list[i]=1
                        var_list[vars]=False
                        #print("THIS",vars)
                    #if the sign of vars is negative in the constraint, then make sure it is false.
                    elif constraints[i][0][vars][0]=='-' and (con_dets[i][2]-variables[vars][1][i])<con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=True:
                                isFeasible=False
                                infeasible_con_list[i]=1
                        var_list[vars]=True

    for i in variables[cur_var][1]:
        #update the constraints list based on the value of the current variable.
        if var_val==0:
            #make sure that it is feasible for the constraint to be assigned true or false.
            if con_dets[i][0]!='>=':
                #if current sum + coefficient>objective goal of constraint and coefficient is positive
                if (con_dets[i][1]+variables[cur_var][1][i])>con_dets[i][3]:
                    isFeasible=False
                    infeasible_con_list[i]=1
            con_dets[i][1]+=variables[cur_var][1][i]
        else:
            #Make sure that assigning the value does not cause conflict
            if con_dets[i][0]!='<=':
                if (con_dets[i][2]-variables[cur_var][1][i])<con_dets[i][3]:
                    isFeasible=False
                    infeasible_con_list[i]=1
            con_dets[i][2]-=variables[cur_var][1][i]
        #check for implications or conflicts caused due to this assignment in the given constraint.
        for vars in constraints[i][0]:
            if decision_strat[vars][0]!=-1:
                if con_dets[i][0]!='>=':
                   #if current sum + coefficient>objective goal of constraint and coefficient is positive
                    if constraints[i][0][vars][0]=='+' and (con_dets[i][1]+variables[vars][0][i])>con_dets[i][3]:
                        if vars in var_list:
                           if var_list[vars]!=False:
                               isFeasible=False
                               infeasible_con_list[i]=1
                        var_list[vars]=False
                    elif constraints[i][0][vars][0]=='-' and (con_dets[i][1]+variables[vars][1][i])>con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=True:
                                isFeasible=False
                                infeasible_con_list[i]=1
                        var_list[vars]=True
                elif con_dets[i][0]!='<=':
                    if constraints[i][0][vars][0]=='+' and (con_dets[i][2]-variables[vars][0][i])<con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=False:
                                isFeasible=False
                                infeasible_con_list[i]=1
                        var_list[vars]=False
                    elif constraints[i][0][vars][0]=='-' and (con_dets[i][2]-variables[vars][1][i])<con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=True:
                                isFeasible=False
                                infeasible_con_list[i]=1
                        var_list[vars]=True

    #Now the var_list should be updated, process the list
    #The list contains the implications of the variable assignment
    #print("The list of implications is:")
    for val in var_list:
        #print("Implication is", val, var_list[val])
        #Iterating over the positive constraints associated with the current variable
        decision_strat[val][0]=(-1)
        for i in variables[val][0]:
            #update the constraints list based on the value of the current variable.
            if var_list[val]==1:
                #make sure that it is feasible for the constraint to be assigned true or false.
                if con_dets[i][0]!='>=':
                    #if current sum + coefficient>objective goal of constraint and coefficient is positive
                    if (con_dets[i][1]+variables[val][0][i])>con_dets[i][3]:
                                isFeasible=False
                                infeasible_con_list[i]=1
                #add value of coefficient to current sum of constraint
                con_dets[i][1]+=variables[val][0][i]
            else:
                #subtract value of coefficient from maximum posible sum of constraints
                #Make sure that assigning the value does not cause conflict
                if con_dets[i][0]!='<=':
                    if (con_dets[i][2]-variables[val][0][i])<con_dets[i][3]:
                                isFeasible=False
                                infeasible_con_list[i]=1
                con_dets[i][2]-=variables[val][0][i]
        #Iterating over the negative constraints associated with the current variable
        for i in variables[val][1]:
            #update the constraints list based on the value of the current variable.
            if var_list[val]==0:
                #make sure that it is feasible for the constraint to be assigned true or false.
                if con_dets[i][0]!='>=':
                    #if current sum + coefficient>objective goal of constraint and coefficient is positive
                    if (con_dets[i][1]+variables[val][1][i])>con_dets[i][3]:
                                isFeasible=False
                                infeasible_con_list[i]=1
                #add value of coefficient to current sum of constraint
                con_dets[i][1]+=variables[val][1][i]
            else:

                #Make sure that assigning the value does not cause conflict
                if con_dets[i][0]!='<=':
                    if (con_dets[i][2]-variables[val][1][i])<con_dets[i][3]:
                                isFeasible=False
                                infeasible_con_list[i]=1
                #subtract value of coefficient from maximum posible sum of constraints
                con_dets[i][2]-=variables[val][1][i]

    #after assigning the values of the assignment, lets check if the whole situation is feasible.
    val_return=infeasible_con_list
    if isFeasible==True:
        #print("____NEXT LEVEL___")
        isAssigned, vals= pbs_solver(decision_strat,constraints,con_dets,variables)
        if isAssigned:
            vals[cur_var]=var_val
            for val in var_list:
                vals[val]=var_list[val]
            return True, vals
        else:
            for i in vals:
                val_return[i]=1
    #reset the values of con_dets to what they were before assignment and the implication
    for i in variables[cur_var][0]:
        if var_val==1:
            con_dets[i][1]-=variables[cur_var][0][i]
        else:
            con_dets[i][2]+=variables[cur_var][0][i]
    for i in variables[cur_var][1]:
        if var_val==0:
            con_dets[i][1]-=variables[cur_var][1][i]
        else:
            con_dets[i][2]+=variables[cur_var][1][i]
    for val in var_list:
        #revert the decision strategy.
        decision_strat[val][0]=1
        for i in variables[val][0]:
            if var_list[val]==1:
                con_dets[i][1]-=variables[val][0][i]
            else:
                con_dets[i][2]+=variables[val][0][i]
        for i in variables[val][1]:
            if var_list[val]==0:
                con_dets[i][1]-=variables[val][1][i]
            else:
                con_dets[i][2]+=variables[val][1][i]
    decision_strat[cur_var][0]=1
    #print("----",cur_var,"lead to infeasibility, back-tracking to its source")
    return False,val_return
    #Maybe instead of just returning value, we need to return implication as well

def print_app_graph(name):
    global scenario
    graph=scenario.graphs[name]
    print("Graph name is ", name)
    print("Number of tasks in Graph is", graph.num_of_tasks)
    i=0
    for task in graph.tasks:
        i+=1
        print("Task", i ," is", task)
        print("List of PEs it can be scheduled on is:")
        for pe in graph.tasks[task].pe_list:
            print("---", pe)
            print("WCET", graph.tasks[task].wcet[pe])
            print("Power", graph.tasks[task].power[pe])
            print("Code_bits", graph.tasks[task].code_bits[pe])

    print("Number of Messages in Graph is ", graph.num_of_arcs)
    i=0
    for arc in graph.arcs:
        i+=1
        print("Arc", i ,"is", arc, "between :")
        print(graph.arcs[arc].task_from, "--->" ,graph.arcs[arc].task_to)

def print_pb_strat(con_graph):
    decision_strat=OrderedDict(deepcopy(sorted(con_graph.pbp_data["complete"].decision_strat.items() , key=lambda x : -x[1][0])))

    print("\n\n\nTHE DECISION STRATEGY IS AS FOLLOWS\n")
    for var in decision_strat:
        print(" ------ Variable",var)
        print("Decision Value",decision_strat[var][0])
        print("Decision Priority",decision_strat[var][1])
    print("\n\n\n")

def gen_dvfslevel(num_levels):
    global scenario
    scenario.dvfs_level = []
    if num_levels == None or num_levels < 3:
        scenario.dvfs_level = [1]
    else:
        #assuming the given frequency is 500 Mhz and the voltage at the given frequency is 1.1 Volt
        freq=500
        volt=1.1
        #ARM processors including A7,A15 all generally have DVFS levels between 200Mhz to 1600 Mhz
        f_up=1600.0/500;
        f_down=200.0/500;
        #The size of each frequency step.
        step_size=(f_up-f_down)/(num_levels-1)
        for i in range(num_levels):
            scenario.dvfs_level.append(f_down+(i*step_size))
    #this creates a list of size dvfs_num_levels
    #the contents of this list will range from [1600/500 to 200/500]
    #now dvfs_level*freq=dvfs_mode_frequency and dvfs_level*volt=dvfs_mode_voltage

#CHANGE
def process_cons(individual):
    #print_pb_strat(con_graph)
    individual.assignment=process_pbp_data(individual)
    gen_phenotype(individual,individual.graph)
    #gen_comp_con_graph(individual,individual.graph)
    #feasiblity_con_graph(con_graph,con_graph.graph)

def make_individual(name="la"):
    individual=creator.Individual()
    individual.graph=name
    gen_genotype(individual,name)
    #print_pb_strat(con_graph)
    individual.assignment=process_pbp_data(individual)
    print("Generated Individual")
    gen_phenotype(individual,name)
    #gen_comp_con_graph(individual,name)
    #feasiblity_con_graph(individual,name)

    return individual

def makepop(graph_name="la", pop_size=5):
    l = []
    for i in range(pop_size):
        l.append(toolbox.individual(name=graph_name))
    print("Population Initiated")
    return l

#CHANGE THESE 3
def evalParams(individual):
    global scenario
    graph=individual.graph
    scenario.graphs[graph].num_of_evals+=1
    energy=0
    task_list=[]
    task_start={}
    task_end={}
    cluster_time={}
    message_list={}
    dvfs_level=1
    message_communication_time=0.001


    # print("\nEVALUATION FOR",graph,"\n")
    # for cluster in individual.task_cluster:
    #     mapped=individual.task_cluster[cluster].mapped_to
    #     print("Cluster",cluster,"is Mapped to PE",mapped)
    #     for task in individual.task_cluster[cluster].tasks:
    #         print("------>",task)
            #print(scenario.graphs[graph].tasks[task].pe_list)
    for cluster in individual.task_cluster:
        cluster_time[cluster]=0

    #Sorting tasks according to priority
    for task in scenario.graphs[graph].tasks:
        task_list.append([scenario.graphs[graph].tasks[task].priority,task])
        task_start[task]=0
    task_list.sort(key=lambda x: x[0])
    #setting lower limit on task start time

    for task_dets in task_list:
        task=task_dets[1]
        cluster=individual.task_to_cluster[task]
        mapped=individual.task_list[task].mapped
        if scenario.dvfs>1:
            dvfs_level=1/scenario.dvfs_level[(individual.task_list[task].dvfs_level)]
        cluster_time[cluster]=(task_start[task]+scenario.graphs[graph].tasks[task].wcet[mapped]*dvfs_level)
        task_end[task]=(task_start[task]+scenario.graphs[graph].tasks[task].wcet[mapped]*dvfs_level)
        for task1 in individual.task_cluster[cluster]:
            if (scenario.graphs[graph].tasks[task1].priority>task_dets[0]):
                if (task_start[task1]<(task_start[task]+(scenario.graphs[graph].tasks[task].wcet[mapped]*dvfs_level))):
                    task_start[task1]=(task_start[task]+(scenario.graphs[graph].tasks[task].wcet[mapped]*dvfs_level))
        for m in scenario.graphs[graph].arcs:
            if scenario.graphs[graph].arcs[m].task_from==task:
                task_to=scenario.graphs[graph].arcs[m].task_to
                cluster_to=individual.task_to_cluster[task_to]
                message_time=0.02
                if cluster_to!=cluster:
                    mapped_to=individual.task_list[cluster_to].mapped
                    tmp1=mapped.split("_")
                    tmp2=mapped_to.split("_")
                    x1=abs(int(tmp1[1])-int(tmp2[1]))
                    y1=abs(int(tmp1[2])-int(tmp2[2]))
                    hops=x1+y1
                    message_time=hops*(scenario.graphs[graph].arcs[m].quant/800)+(hops-1)*(0.002)
                    message_list[m]=hops
                if task_start[task_to]<(task_start[task]+(scenario.graphs[graph].tasks[task].wcet[mapped]*dvfs_level)+message_time):
                    task_start[task_to]=(task_start[task]+(scenario.graphs[graph].tasks[task].wcet[mapped]*dvfs_level)+message_time)

    max_time=0
    for cluster in cluster_time:
        if(cluster_time[cluster]>max_time):
            max_time=cluster_time[cluster]

    #Computing the total energy usage
    for cluster in individual.task_cluster:
        mapped=individual.task_list[cluster].mapped
        for task in individual.task_cluster[cluster]:
            if scenario.dvfs>1:
                #print((individual.dvfs_level[task]))
                dvfs_level=scenario.dvfs_level[(individual.task_list[task].dvfs_level)]
            wcet=scenario.graphs[graph].tasks[task].wcet[mapped]
            power=scenario.graphs[graph].tasks[task].power[mapped]
            energy+=(wcet*power*dvfs_level*dvfs_level)
    for m in message_list:
        energy+=((message_list[m]*100-(63))*scenario.graphs[graph].arcs[m].quant)/(1e6)

    inc=0
    print("\nEVALUATION FOR",graph,"\n")
    for cluster in individual.task_cluster:
        inc+=1
        mapped=individual.task_list[cluster].mapped
        print("Cluster",inc,"is Mapped to PE",mapped)
        for task in individual.task_cluster[cluster]:
            print("------>",task)
            print("start time",task_start[task])
            print("end time",task_end[task])
            if scenario.dvfs>1:
                print("DVFS Level is", (individual.task_list[task].dvfs_level))
        print("----------------------------------")
    # for m in message_list:
    #     print(m,"has hop distance",message_list[m])
    print("The total execution time is",max_time,)
    print("The total energy is",energy,"\n")
    return (energy,max_time,)

def matefunc(ind1,ind2):
    #print("crossover starts")
    for task in ind1.pbp_data:
        if random.randint(0,1)==1:
            temp=ind1.pbp_data[task]
            ind1.pbp_data[task]=ind2.pbp_data[task]
            ind2.pbp_data[task]=temp
    #process constraints
    process_cons(ind1)
    process_cons(ind2)
    return ind1, ind2

def mutatefunc(ind,indpb=0.1):
    #print("Mutate starts")
    for task in ind.pbp_data:
        for a in ind.pbp_data[task].decision_strat:
            if random.random() < indpb:
                ind.pbp_data[task].decision_strat[a][0]+=ind.pbp_data[task].max_priority
                if ind.pbp_data[task].decision_strat[a][0]>ind.pbp_data[task].max_priority:
                    ind.pbp_data[task].max_priority=ind.pbp_data[task].decision_strat[a][0]
    ind.generation+=1
    process_cons(ind)
    #process constraints
    return ind

creator.create("Fitness", base.Fitness, weights=(-1.0,-1.0,))
creator.create("Individual",Individual_data,fitness=creator.Fitness)

toolbox = base.Toolbox()

toolbox.register("individual",make_individual)
toolbox.register("population",makepop)
#----------
# Operator registration
#----------
# register the goal / fitness function
toolbox.register("evaluate", evalParams)
# register the crossover operator
toolbox.register("mate", matefunc)
# register a mutation operator with a probability to
# flip each attribute/gene of 0.05
toolbox.register("mutate",mutatefunc, indpb=0.05)
#fittest of the individuals is selected for breeding..
toolbox.register("select", tools.selTournament)
#toolbox.register("select", tools.selNSGA2)

#intialising the statistics functions

stats = tools.Statistics(key=lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean, axis=0)
stats.register("std", numpy.std, axis=0)
stats.register("min", numpy.min, axis=0)
stats.register("max", numpy.max, axis=0)

def main():
    total_start_time=time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("input_tgff", help="*.tgff file to parse")
    parser.add_argument("--tg", help="*name of task_graph",default="TASK_GRAPH")
    parser.add_argument("--modular","-m",default=0,help="Use modular or complete clustering, Modular=1/Complete=0")
    parser.add_argument("--core", help="name of core/PE", default="CLIENT_PE")
    parser.add_argument("-d", "--dir",default="./output", help="output directory")
    parser.add_argument("--dvfs_level","--dvfs",action="store", dest="dvfs_num_levels", type=int, default=None, help="The number of dvfs_levels possible for each processor")
    args = parser.parse_args()
    global scenario
    scenario = Complete_Scenario()
    #saving the number of dvfs levels taken as input
    scenario.dvfs=args.dvfs_num_levels
    #processing the input tgff file
    with open(args.input_tgff) as input_file:
        for block in get_blocks(input_file):
            process_block(block,args.tg,args.core)

    assign_priorities()
    populate_message_params()
    generate_noc(2,2)
    populate_task_params()
    if args.dvfs_num_levels!=None:
        scenario.dvfs=args.dvfs_num_levels
    else:
        scenario.dvfs=1
    gen_dvfslevel(args.dvfs_num_levels)
    phase=0
    left_ext=args.input_tgff.rfind('/')
    right_ext=args.input_tgff.rfind('.')
    file_name=args.input_tgff[left_ext+1:right_ext]
    #Processing each graph seperately
    for graph in scenario.graphs:
        #plot_app_graph(graph,phase,file_name,args.dir)
        # print_app_graph(graph)


        pop=None
        print(f"Generating Population for {graph}")
        start_time=time.time()
        pop = toolbox.population(graph_name=graph,pop_size=100)
        # CXPB  is the probability with which two individuals
        #       are crossed
        #
        # MUTPB is the probability for mutating an individual
        CXPB, MUTPB = 0.2, 0.03

        print("Start of evolution", graph)
        # Evaluate the entire population
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(pop))

        fits = [ind.fitness.values[0] for ind in pop]
        # Variable keeping track of the number of generations
        g = 0
        #initialising the Logbook
        logbook = tools.Logbook()
        #initialising the ParetoFront
        # pf= tools.HallOfFame(maxsize=100)
        pf= tools.ParetoFront()
        # Begin the evolution
        while g < 5:
            # A new generation
            g = g + 1
            print("-- Generation %i --" % g)

            # Select the next generation individuals
            offspring = toolbox.select(pop, len(pop),tournsize=3)
            #offspring = toolbox.select(pop, len(pop))
            # Clone the selected individuals
            offspring = list(map(toolbox.clone, offspring))

            # Apply crossover and mutation on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):

                # cross two individuals with probability CXPB
                if random.random() < CXPB:
                    toolbox.mate(child1, child2)
                    #print("mate runs")
                    # fitness values of the children
                    # must be recalculated later
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:

                # mutate an individual with probability MUTPB
                if random.random() < MUTPB:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            #print("  Evaluated %i individuals" % len(invalid_ind))

            # The population is entirely replaced by the offspring
            pop[:] = offspring

            record = stats.compile(pop)
            pf.update(pop)
            hv = hypervolume(pop, [0.0,0.0])
            best=tools.selBest(pop, 1)[0]
            logbook.record(gen=g, evals=100 , hv=hv, best=best.fitness.values, **record)

            #Gather all the fitnesses in one list and print the stats


            fits0 = [ind.fitness.values[0] for ind in pop]
            length = len(pop)
            mean = sum(fits0) / length
            sum2 = sum(x*x for x in fits0)
            std = abs(sum2 / length - mean**2)**0.5
            print(" Values of Energy in microwatt/second")
            print("   Min %s" % min(fits0))
            print("   Max %s" % max(fits0))
            print("   Avg %s" % mean)
            print("   Std %s" % std)
            fits0 = [ind.fitness.values[1] for ind in pop]
            length = len(pop)
            mean = sum(fits0) / length
            sum2 = sum(x*x for x in fits0)
            std = abs(sum2 / length - mean**2)**0.5
            print(" Values of Execution time in microseconds")
            print("   Min %s" % min(fits0))
            print("   Max %s" % max(fits0))
            print("   Avg %s" % mean)
            print("   Std %s" % std)



        # logbook.header = "gen", "avg", "max","min"
        # print(logbook)
        print("-- End of (successful) evolution --")
        end_time=time.time()
        print("---------GENERATING STATISTICS---------")
        print("\nTotal Seconds taken for evaluation are", (end_time-start_time))
        print("Total Number of Evaluations are",scenario.graphs[graph].num_of_evals,"\n")
        # Making Plots
        phase_name=f"{file_name}_{phase}"

        gen= logbook.select("gen")
        fitness_avg = logbook.select("avg")
        avg_energy, avg_time = zip(*fitness_avg)
        fitness_min = logbook.select("min")
        min_energy, min_time = zip(*fitness_min)
        hv = logbook.select("hv")
        fitness_best=logbook.select("best")
        best_energy, best_time = zip(*fitness_best)


        stats_plot_name=f"{args.dir}/{phase_name}_stats.png"
        hv_plot_name=f"{args.dir}/{phase_name}_best.png"
        pf_plot_name=f"{args.dir}/{phase_name}_pf.png"

        fig, (ax1,ax2,ax3) = plt.subplots(3)
        #Plotting Energy stats for each generation
        line1 = ax1.plot(gen, avg_energy, "b-", label="Average Energy")
        ax1.set_xlabel("Generation")
        ax1.set_ylabel("Energy", color="b")
        for tl in ax1.get_yticklabels():
            tl.set_color("b")
        line2 = ax1.plot(gen, min_energy, "r-", label="Minimum Energy")
        lns = line1 + line2
        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc="center right")
        #Plotting Time stats for each generation
        line1 = ax2.plot(gen, avg_time, "b-", label="Average Time")
        ax2.set_xlabel("Generation")
        ax2.set_ylabel("Execution Time", color="b")
        for tl in ax2.get_yticklabels():
            tl.set_color("r")
        line2 = ax2.plot(gen, min_time, "r-", label="Minimum Time")
        lns = line1 + line2
        labs = [l.get_label() for l in lns]
        ax2.legend(lns, labs, loc="center right")
        #Plotting Best individuals of each generation
        line1 = ax3.plot(gen, best_time, "b-", label="Best Time")
        ax3.set_xlabel("Generation")
        ax3.set_ylabel("Execution Time", color="b")
        for tl in ax3.get_yticklabels():
            tl.set_color("b")
        ax4 = ax3.twinx()
        line2 = ax4.plot(gen, best_energy, "r-", label="Best Energy")
        ax4.set_ylabel("Total Energy", color="r")
        for tl in ax4.get_yticklabels():
            tl.set_color("r")
        lns = line1 + line2
        labs = [l.get_label() for l in lns]
        ax3.legend(lns, labs, loc="center right")
        plt.savefig(stats_plot_name)
        plt.close()
        #plt.show()

        # fig, ax1 = plt.subplots()
        # line1 = ax1.plot(gen, hv, "b-", label="Hypervolume")
        # ax1.set_xlabel("Generation")
        # ax1.set_ylabel("HyperVolume wrt 0,0", color="b")
        # labs = [l.get_label() for l in line1]
        # ax1.legend(lns, labs, loc="center right")
        # plt.savefig(hv_plot_name)
        # plt.close()
        #plt.savefig(stats_plot_name)

        energy_pf = [ind.fitness.values[0] for ind in pf]
        time_pf = [ind.fitness.values[1] for ind in pf]
        fig, ax1 = plt.subplots()
        line1 = ax1.plot(energy_pf, time_pf, "b-", label="ParetoFront")
        ax1.set_xlabel("Energy")
        ax1.set_ylabel("Execution Time", color="b")
        labs = [l.get_label() for l in line1]
        ax1.legend(lns, labs, loc="center right")

        plt.savefig(pf_plot_name)
        plt.close()

        best_ind = tools.selBest(pop, 1)[0]
        #plot_constraint_graph(best_ind,graph,file_name,phase,dir)
        print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
        phase+=1
    total_end_time=(time.time()-total_start_time)
    print("Discrete Constrainted Meta-Heuristic successful !!!")
    print("Total DSE time is", total_end_time)
    return
if __name__ == '__main__':
    main()
