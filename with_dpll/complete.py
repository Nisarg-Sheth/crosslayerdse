import os
import sys
import re
import argparse
import random
import subprocess
from graphviz import Digraph
from deap import *
from old_source import *
from copy import deepcopy

scenario = None

random.seed(123)

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


    elif core in block[0]:
        core_name = None
        i = 0
        core_name= block[0].strip('@').strip('{').replace(" ","")
        #print(core_name)
        scenario.all_tables[core_name]=Table(core_name,block[1].strip('#'),block[2].strip('#'),block[4].strip('#'))
        for i in range(5, len(block)):
            if not block[i].startswith('#'):
                scenario.all_tables[core_name].add_row(block[i])
    elif "HYPERPERIOD" in block[0]:
        scenario.hyperperiod= float(block[0].strip('@HYPERPERIOD '))

def populate_task_params():
    global scenario
    for graph in scenario.graphs:
        for task in scenario.graphs[graph].tasks:
            type_of_task=scenario.graphs[graph].tasks[task].type
            for table in scenario.tables:
                if scenario.tables[table].values[type_of_task][0]==type_of_task:
                    if int(scenario.tables[table].values[type_of_task][2])==1:
                        #adding the PE to the pe_list of each task
                        scenario.graphs[graph].tasks[task].pe_list.append(table)
                        #adding the processing time on the PE for each task
                        scenario.graphs[graph].tasks[task].wcet[table]=float(scenario.tables[table].values[type_of_task][3])
                        #adding the task_power on the PE to the task arc_details
                        scenario.graphs[graph].tasks[task].power[table]=float(scenario.tables[table].values[type_of_task][6])
                        #adding code bits to the task details
                        scenario.graphs[graph].tasks[task].code_bits[table]=float(scenario.tables[table].values[type_of_task][5])
                        #adding preemeption_time
                        scenario.graphs[graph].tasks[task].preempt_time[table]=float(scenario.tables[table].values[type_of_task][4])

#generate the constraint graph from the ILP
def generate_con_graph(input_file, graph):
    global scenario
    scenario.constraint_graphs[graph] = Constraint_graph()
    slave_list = []
    master_list = []
    map_list = []
    c_list = []
    sl_list = []
    hop_list = []
    with open(input_file) as file:
        for line in file:
            if not line.startswith('#'):
                parts=line.split()
                if parts[0].endswith("_master") and parts[1] is "1":
                    ext_id = parts[0].rfind("_")
                    master_list.append(parts[0][:ext_id])
                elif parts[0].endswith("_slave") and parts[1] is "1":
                    ext_id = parts[0].rfind("_")
                    slave_list.append(parts[0][:ext_id])
                elif parts[0].startswith("map_") and parts[1] is "1":
                    map_list.append(parts[0][4:])
                elif parts[0].startswith("C_") and parts[1] is "1":
                    c_list.append(parts[0][2:])
                elif parts[0].startswith("sl_") and parts[1] is "1":
                    sl_list.append(parts[0][3:])
                elif parts[0].startswith("hop_") and parts[1] is "1":
                    hop_list.append(parts[0][4:])

    for m in master_list:
        scenario.constraint_graphs[graph].task_cluster[m]=Task_cluster()
        scenario.constraint_graphs[graph].task_cluster[m].tasks.append(m)
        scenario.constraint_graphs[graph].task_to_cluster[m]=m
    for c in c_list:
        tasks=c.split("_",1)
        if tasks[1] in scenario.constraint_graphs[graph].task_cluster:
            scenario.constraint_graphs[graph].task_cluster[tasks[1]].tasks.append(tasks[0])
            scenario.constraint_graphs[graph].task_to_cluster[tasks[0]]=tasks[1]
    for m in map_list:
        a=m.split("_",1)
        scenario.constraint_graphs[graph].task_cluster[a[0]].mapped_to=a[1]

    for sl in sl_list:
        a=sl.split("_",1)
        task_from = scenario.graphs[graph].arcs[a[1]].task_from
        task_to = scenario.graphs[graph].arcs[a[1]].task_to
        if scenario.constraint_graphs[graph].task_to_cluster[task_to] != scenario.constraint_graphs[graph].task_to_cluster[task_from]:
            scenario.constraint_graphs[graph].messages[a[1]]=Message()
            scenario.constraint_graphs[graph].messages[a[1]].cluster_from=scenario.constraint_graphs[graph].task_to_cluster[task_from]
            scenario.constraint_graphs[graph].messages[a[1]].cluster_to=scenario.constraint_graphs[graph].task_to_cluster[task_to]
            scenario.constraint_graphs[graph].messages[a[1]].sl=int(a[0])

    for hop in hop_list:
        a=hop.split("_",1)
        if a[1] in scenario.constraint_graphs[graph].messages:
            scenario.constraint_graphs[graph].messages[a[1]].hop=int(a[0])

#Plotting the constraint graph
def plot_constraint_graph(graph,phase,dir):
    constraint_g = Digraph(comment = graph, format='png')
    for task in scenario.constraint_graphs[graph].task_cluster:
        to_show=""
        mapped_to = scenario.constraint_graphs[graph].task_cluster[task].mapped_to
        for a in scenario.constraint_graphs[graph].task_cluster[task].tasks:
            to_show+=f"{a}(dvfs_level {scenario.constraint_graphs[graph].dvfs_level[a]}), "
        to_show= f"[{to_show}]\n"+mapped_to
        constraint_g.node(str(task),label=to_show)
    for m in scenario.constraint_graphs[graph].messages:
        to_show="m"
        to_show=to_show + "\n"+str(scenario.constraint_graphs[graph].messages[m].sl)
        to_show=to_show + "\n"+str(scenario.constraint_graphs[graph].messages[m].hop)
        constraint_g.node(m,label=to_show)
        constraint_g.edge(str(scenario.constraint_graphs[graph].messages[m].cluster_from), m)
        constraint_g.edge(m,str(scenario.constraint_graphs[graph].messages[m].cluster_to))
    constraint_g.render(f"{dir}/con_graph_plot{phase}.view",view=False)

def plot_app_graph(graph,phase,dir):
    app_g = Digraph(comment = graph,format='png')
    for task in scenario.graphs[graph].tasks:
        app_g.node(str(task),label=task)
    for m in scenario.graphs[graph].arcs:
        app_g.node(m,label=m)
        app_g.edge(scenario.graphs[graph].arcs[m].task_from,m)
        app_g.edge(m,scenario.graphs[graph].arcs[m].task_to)
    app_g.render(f"{dir}/app_graph_plot{phase}.view",view=False)

def process_ILP1(input_file,output_file, graph):
    global scenario
    scenario.constraint_graphs[graph] = Constraint_graph()
    #Processing the solution file
    with open(input_file) as file:
        for line in file:
            if not line.startswith('#'):
                vals=line.split()
                if int(vals[1])==1:
                    a=vals[0].rsplit("_",1)
                    if a[1]=="iscluster":
                        scenario.constraint_graphs[graph].num_of_clusters+=1
                    elif int(a[1]) in scenario.constraint_graphs[graph].task_cluster:
                        scenario.constraint_graphs[graph].task_cluster[int(a[1])].tasks.append(a[0])
                        scenario.constraint_graphs[graph].task_to_cluster[a[0]]=int(a[1])
                    else:
                        scenario.constraint_graphs[graph].task_cluster[int(a[1])]=Task_cluster()
                        scenario.constraint_graphs[graph].task_cluster[int(a[1])].tasks.append(a[0])
                        scenario.constraint_graphs[graph].task_to_cluster[a[0]]=int(a[1])


    #Adding the possible PEs to each task cluster
    for a in scenario.constraint_graphs[graph].task_cluster:
        i=0
        pe_dict={}
        for task in scenario.constraint_graphs[graph].task_cluster[a].tasks:
            i+=1
            for pe in scenario.graphs[graph].tasks[task].pe_list:
                if pe in pe_dict:
                    pe_dict[pe]+=1
                else:
                    pe_dict[pe]=1
        for pe in pe_dict:
            if pe_dict[pe]==i:
                scenario.constraint_graphs[graph].task_cluster[a].can_be_mapped.append(pe)

        #Making sure we don't exceed the hyperperiod on the PE
        #this is an additional check
        for pe in scenario.constraint_graphs[graph].task_cluster[a].can_be_mapped:
            tot_exec_t=0
            for task in scenario.constraint_graphs[graph].task_cluster[a].tasks:
                tot_exec_t+=scenario.graphs[graph].tasks[task].wcet[pe]
            if tot_exec_t > scenario.hyperperiod:
                scenario.constraint_graphs[graph].task_cluster[a].can_be_mapped.remove(pe)
                #print(pe + " removed")

    #Making sure that the messages between the same PEs is ignored in the next ILP
    #Untested code bits here
    for arc in scenario.graphs[graph].arcs:
        task_from=scenario.graphs[graph].arcs[arc].task_from
        task_to=scenario.graphs[graph].arcs[arc].task_to
        #print(task_from+"->"+task_to)
        if scenario.constraint_graphs[graph].task_to_cluster[task_to] != scenario.constraint_graphs[graph].task_to_cluster[task_from]:
            scenario.constraint_graphs[graph].messages[arc]=Message()
            scenario.constraint_graphs[graph].messages[arc].cluster_to=scenario.constraint_graphs[graph].task_to_cluster[task_to]
            scenario.constraint_graphs[graph].messages[arc].cluster_from=scenario.constraint_graphs[graph].task_to_cluster[task_from]

    #add constraints to problem...
    is_feasible=True
    constraints_to_add=[]
    for a in scenario.constraint_graphs[graph].task_cluster:
        if scenario.constraint_graphs[graph].task_cluster[a].can_be_mapped==None or not scenario.constraint_graphs[graph].task_cluster[a].can_be_mapped:
            #the current cluster is no longer feasible

            is_feasible=False
            con_val= "added_constraint"
            scenario.num_of_added_con+=1
            con = f"{con_val}_{str(scenario.num_of_added_con)} : "
            line =""

            i=0
            for task in scenario.constraint_graphs[graph].task_cluster[a].tasks:
                line += f" + 1 {task}_{str(a)} "
                i+=1
            line+=f" <= {i}"
            constraints_to_add.append(con+line)

    edit_ILP(output_file,constraints_to_add,None)
    return is_feasible

#ILP for assigning the Resource type to cluster and the dvfs mode to each task.
def generate_ILP2(output_file, graph):
    global scenario
    num_of_con=0;
    con_val= "constraint"
    with open(output_file, 'w') as f:
        #defining the minimization problem
        f.write("Minimize\n")
        line="problem: "
        for cluster in scenario.constraint_graphs[graph].task_cluster:
            for pe in scenario.constraint_graphs[graph].task_cluster[cluster].can_be_mapped:
                energy=0
                for task in scenario.constraint_graphs[graph].task_cluster[cluster].tasks:
                    energy+=(scenario.graphs[graph].tasks[task].wcet[pe]*scenario.graphs[graph].tasks[task].power[pe])
                line+=f"+ {energy} {pe}_{cluster} "
        f.write(line+"\n")
        f.write("Subject To\n")
        i=1
        for cluster in scenario.constraint_graphs[graph].task_cluster:
            num_of_con+=1
            con = f"{con_val}_{str(num_of_con)} : "
            line=""
            for pe in scenario.constraint_graphs[graph].task_cluster[cluster].can_be_mapped:
                line+=f"+ 1 {pe}_{cluster} "
            line+=f" = 1 "
            f.write(con+line+"\n")

            #Declare the variables as binary
        f.write("\n")
        f.write("Binary\n\n")
        num_var=0
        i=1
        for cluster in scenario.constraint_graphs[graph].task_cluster:
            for pe in scenario.constraint_graphs[graph].task_cluster[cluster].can_be_mapped:
                line=f"{pe}_{cluster}\n"
                f.write(line)
    print(f"ILP resource mapping written for graph")

def process_ILP2(input_file,output_file, graph):
    global scenario
    with open(input_file) as file:
        for line in file:
            if not line.startswith('#'):
                vals=line.split()
                if int(vals[1])==1:
                    more_vals=vals[0].rsplit("_",1)
                    scenario.constraint_graphs[graph].task_cluster[int(more_vals[1])].mapped_to=more_vals[0]

#ILP for assigning the Resource type to cluster and the dvfs mode to each task.
#Still incomplete
def generate_ILP3(output_file, graph, num_levels):
    #only perform dvfs if 3 or more levels
    if num_levels < 3:
        print("Didnt have proper dvfs input, no dvfs assumed")
        return

    global scenario
    num_of_con=0;
    con_val= "constraint"

    with open(output_file, 'w') as f:
        f.write("Minimize\n")
        line="problem: src_0"

        f.write(line+"\n")
        f.write("Subject To\n")
        for cluster in scenario.constraint_graphs[graph].task_cluster:
            for task in scenario.constraint_graphs[graph].task_cluster[cluster].tasks:
                line=""
                num_of_con+=1
                con = f"{con_val}_{str(num_of_con)} : "
                for d in range(num_levels):
                    line+=f" + 1 {task}_{d}"
                line+=f" = 1 "
                f.write(con+line+"\n")

        #Declare the variables as binary
        f.write("\n")
        f.write("Binary\n\n")
        num_var=0
        i=1
        for cluster in scenario.constraint_graphs[graph].task_cluster:
            for task in scenario.constraint_graphs[graph].task_cluster[cluster].tasks:
                for d in range(num_levels):
                    line=f"{task}_{d}\n"
                    f.write(line)
    print(f"ILP dvfs_level written for graph")

def process_ILP3(input_file,output_file, graph,num_levels):
    global scenario
    dvfs_levels = []
    #assuming the given frequency is 500 Mhz and the voltage at the given frequency is 1.1 Volt
    freq=500
    volt=1.1
    #ARM processors including A7,A15 all generally have DVFS levels between 200Mhz to 1600 Mhz
    f_up=1600.0/500;
    f_down=200.0/500;
    #The size of each frequency step.
    step_size=(f_up-f_down)/(num_levels-1)
    for i in range(num_levels):
        dvfs_levels.append(f_down+(i*step_size))
    #this creates a list of size dvfs_num_levels
    #the contents of this list will range from [1600/500 to 200/500]
    #now dvfs_level*freq=dvfs_mode_frequency and dvfs_level*volt=dvfs_mode_voltage
    with open(input_file) as file:
        for line in file:
            if not line.startswith('#'):
                vals=line.split()
                if int(vals[1])==1:
                    more_vals=vals[0].rsplit("_",1)
                    scenario.constraint_graphs[graph].dvfs_level[more_vals[0]]=dvfs_levels[more_vals[1]]

#ILP for assigning the Resource type to cluster and the dvfs mode to each task.
def generate_ILP_withdvfs(output_file, graph,num_levels):
    global scenario
    num_of_con=0;
    con_val= "constraint"
    with open(output_file, 'w') as f:
        #defining the minimization problem
        f.write("Maximize\n")
        line="problem: "
        # for cluster in scenario.constraint_graphs[graph].task_cluster:
        #     for pe in scenario.constraint_graphs[graph].task_cluster[cluster].can_be_mapped:
        #         energy=0
        #         for task in scenario.constraint_graphs[graph].task_cluster[cluster].tasks:
        #             energy+=(scenario.graphs[graph].tasks[task].wcet[pe]*scenario.graphs[graph].tasks[task].power[pe])
        #         line+=f"+ {energy} {pe}_{cluster} "
        #random resource allocation
        for cluster in scenario.constraint_graphs[graph].task_cluster:
            line+= f" + 1 {scenario.constraint_graphs[graph].task_cluster[cluster].can_be_mapped[random.randint(0,(len(scenario.constraint_graphs[graph].task_cluster[cluster].can_be_mapped)-1))]}_{cluster} "
        #random dvfs_levels
        if num_levels == None or num_levels < 3:
            bad_code=1
        else:
            for task in scenario.graphs[graph].tasks:
                line+=f" + 1 {task}_{random.randint(0,(num_levels-1))}"
        f.write(line+"\n")
        f.write("Subject To\n")
        i=1
        for cluster in scenario.constraint_graphs[graph].task_cluster:
            num_of_con+=1
            con = f"{con_val}_{str(num_of_con)} : "
            line=""
            for pe in scenario.constraint_graphs[graph].task_cluster[cluster].can_be_mapped:
                line+=f"+ 1 {pe}_{cluster} "
            line+=f" = 1 "
            f.write(con+line+"\n")
        if num_levels == None or num_levels < 3:
            print("No dvfs assumed")
        else:
            for cluster in scenario.constraint_graphs[graph].task_cluster:
                for task in scenario.constraint_graphs[graph].task_cluster[cluster].tasks:
                    line=""
                    num_of_con+=1
                    con = f"{con_val}_{str(num_of_con)} : "
                    for d in range(num_levels):
                        line+=f" + 1 {task}_{d}"
                    line+=f" = 1 "
                    f.write(con+line+"\n")
            #Declare the variables as binary
        f.write("\n")
        f.write("Binary\n\n")
        num_var=0
        i=1
        for cluster in scenario.constraint_graphs[graph].task_cluster:
            for pe in scenario.constraint_graphs[graph].task_cluster[cluster].can_be_mapped:
                line=f"{pe}_{cluster}\n"
                f.write(line)
        if num_levels == None or num_levels < 3:
            print("No dvfs assumed")
        else:
            for cluster in scenario.constraint_graphs[graph].task_cluster:
                for task in scenario.constraint_graphs[graph].task_cluster[cluster].tasks:
                    for d in range(num_levels):
                        line=f"{task}_{d}\n"
                        f.write(line)
    print(f"ILP resource mapping written for graph")

def process_ILP_withdvfs(input_file,output_file, graph,num_levels):
    global scenario
    dvfs_levels = []
    if num_levels == None or num_levels < 3:
        dvfs_levels = [1]
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
            dvfs_levels.append(f_down+(i*step_size))
    #this creates a list of size dvfs_num_levels
    #the contents of this list will range from [1600/500 to 200/500]
    #now dvfs_level*freq=dvfs_mode_frequency and dvfs_level*volt=dvfs_mode_voltage
    with open(input_file) as file:
        for line in file:
            if not line.startswith('#'):
                vals=line.split()
                if int(vals[1])==1:
                    more_vals=vals[0].rsplit("_",1)
                    if more_vals[0] in scenario.tables:
                        scenario.constraint_graphs[graph].task_cluster[int(more_vals[1])].mapped_to=more_vals[0]
                    else:
                        scenario.constraint_graphs[graph].dvfs_level[more_vals[0]]=int(more_vals[1])
#function to add constraints and variables to the ILP formulation
# takes three input the file name, a list of constraints and a list of variables.

def edit_ILP(input_file,constraints,vars):
    global scenario
    if constraints!=None:
        #add constraints
        with open(input_file, 'r+') as f:
            contents=f.readlines()
            for constraint in constraints:
                contents.insert(3,f"{constraint}\n")
            f.seek(0)
            f.writelines(contents)
    if vars!=None:
        #add variables
        with open(input_file, 'a') as f:
            for var in vars:
                f.write(f"{var}\n")

def generate_ILP(output_file, graph):
    global scenario
    master_list=[]
    slave_list=[]
    task_list=[]
    c_list=[]
    service_level=10
    hop_level=(4*4)-2
    map_list=[]
    for task in graph.tasks:
        master_list.append(task+"_master")
        slave_list.append(task+"_slave")
        map_list.append(graph.tasks[task].pe_list)
        task_list.append(task)
    for task1 in graph.tasks:
        for task2 in graph.tasks:
            c_list.append("C_"+task1+"_"+task2)
    num_of_con=0;
    con_val= "constraint"
    pluss=" + "
    minuss=" - "
    equalss=" = "
    lessthan=" <= "
    greaterthan=" >= "


    with open(output_file, 'w') as f:
        f.write("Maximize\n")
        f.write("problem: "+master_list[1]+ " + "+master_list[2]+" + "+master_list[3]+"\n")
        f.write("Subject To"+"\n")
        for i in range(len(graph.tasks)):

            # Tslave+ Tmaster = 1
            num_of_con+=1
            con = con_val+"_"+str(num_of_con)+ " : "
            line=pluss+" 1 "+master_list[i]+pluss+" 1 "+slave_list[i]+equalss+"1"
            f.write(con+line+"\n")

            # Connnected in Vertical direction,
            num_of_con+=1
            con = con_val+"_"+str(num_of_con)+ " : "
            line=pluss+str(i)+" "+master_list[i]
            for j in range(i):
                line=line+pluss+" 1 "+c_list[(i*graph.num_of_tasks)+j]
            line = line + lessthan + str(i)
            f.write(con+line+"\n")

            # Connected in Horizontal direction,
            num_of_con+=1
            con = con_val+"_"+str(num_of_con)+ " : "
            line=pluss+str(graph.num_of_tasks-(i+1))+" "+slave_list[i]
            for j in range((i+1),graph.num_of_tasks):
                line=line+pluss+" 1 "+c_list[(j*graph.num_of_tasks)+i]
            line = line + lessthan +str(graph.num_of_tasks-(i+1))
            f.write(con+line+"\n")

            # Is slave only connected to one??
            num_of_con+=1
            con = con_val+"_"+str(num_of_con)+ " : "
            line = minuss + " 1 "+slave_list[i]
            for j in range(i):
                line=line+pluss+" 1 "+c_list[(i*graph.num_of_tasks)+j]
            line = line + equalss + "0"
            f.write(con+line+"\n")

            #Mapping the Tmasters to Resources
            num_of_con+=1
            con = con_val+"_"+str(num_of_con)+ " : "
            line = minuss + " 1 "+master_list[i]
            for j in map_list[i]:
                line = line + pluss + " 1 " +"map_"+task_list[i]+"_"+j
            line = line + equalss + "0"
            f.write(con+line+"\n")

            #verifying that mapping is not bad.
            for j in range(i):
                num_of_con+=1
                con = con_val+"_"+str(num_of_con)+ " : "
                line=minuss+" 1 "+c_list[(i*graph.num_of_tasks)+j]
                for pe in map_list[i]:
                    if pe in map_list[j]:
                        line = line + pluss + " 1 " +"map_"+task_list[j]+"_"+pe
                line = line + greaterthan + "0"
                f.write(con+line+"\n")
            for j in range((i+1),graph.num_of_tasks):
                num_of_con+=1
                con = con_val+"_"+str(num_of_con)+ " : "
                line=minuss+" 1 "+c_list[(i*graph.num_of_tasks)+j]
                for pe in map_list[i]:
                    if pe in map_list[j]:
                        line = line + pluss + " 1 " +"map_"+task_list[i]+"_"+pe
                line = line + greaterthan + "0"
                f.write(con+line+"\n")

        for m in graph.arcs:

            #service level for each message
            num_of_con+=1
            con = con_val+"_"+str(num_of_con)+ " : "
            line=""
            for j in range(service_level):
                line= line +pluss+" 1 "+"sl_"+str(j)+"_"+m
            line = line + equalss + "1"
            f.write(con+line+"\n")

            #maximum hop distance for each message
            num_of_con+=1
            con = con_val+"_"+str(num_of_con)+ " : "
            line=""
            for j in range(hop_level):
                line= line +pluss+" 1 "+"hop_"+str(j+1)+"_"+m
            line = line + equalss + "1"
            f.write(con+line+"\n")

        print("The number of constraints: "+str(num_of_con))
        #Declare the variables as binary
        f.write("\n")
        f.write("Binary"+"\n\n")
        num_var=0
        for i in range(len(graph.tasks)):
            f.write(master_list[i]+"\n")
            num_var+=1
            f.write(slave_list[i]+"\n")
            num_var+=1
            for j in range(i):
                f.write(c_list[(i*graph.num_of_tasks)+j]+"\n")
                num_var+=1
            for j in range((i+1),graph.num_of_tasks):
                f.write(c_list[(i*graph.num_of_tasks)+j]+"\n")
                num_var+=1
            for j in map_list[i]:
                f.write("map_"+task_list[i]+"_"+j+"\n")
                num_var+=1

        for m in graph.arcs:
            for j in range(service_level):
                f.write("sl_"+str(j)+"_"+m+"\n")
                num_var+=1
            for j in range(hop_level):
                f.write("hop_"+str(j+1)+"_"+m+"\n")
                num_var+=1
        print("The number of variables: "+str(num_var))
        f.write("End\n")

def generate_noc(length,breadth):
    global scenario
    for i in range(length):
        l=[]
        for j in range(breadth):
            temp=random.sample(scenario.all_tables.keys(),1)
            scenario.tables[temp[0]]=scenario.all_tables[temp[0]]
            l.append(temp[0])
        scenario.NOC.append(l)


def process_clustering(graph):
    global scenario
    for var in scenario.constraint_graphs[graph].pbp_data["cluster"].assignment:
        a = var.rsplit("_",1)
        if int(a[1]) in scenario.constraint_graphs[graph].task_cluster:
            scenario.constraint_graphs[graph].task_cluster[int(a[1])].tasks.append(a[0])
            scenario.constraint_graphs[graph].task_to_cluster[a[0]]=int(a[1])
        else:
            scenario.constraint_graphs[graph].task_cluster[int(a[1])]=Task_cluster()
            scenario.constraint_graphs[graph].task_cluster[int(a[1])].tasks.append(a[0])
            scenario.constraint_graphs[graph].task_to_cluster[a[0]]=int(a[1])

    #Adding the possible PEs to each task cluster
    for a in scenario.constraint_graphs[graph].task_cluster:
        i=0
        pe_dict={}
        for task in scenario.constraint_graphs[graph].task_cluster[a].tasks:
            i+=1
            for pe in scenario.graphs[graph].tasks[task].pe_list:
                if pe in pe_dict:
                    pe_dict[pe]+=1
                else:
                    pe_dict[pe]=1
        for pe in pe_dict:
            if pe_dict[pe]==i:
                scenario.constraint_graphs[graph].task_cluster[a].can_be_mapped.append(pe)

        #Making sure we don't exceed the hyperperiod on the PE
        #this is an additional check
        for pe in scenario.constraint_graphs[graph].task_cluster[a].can_be_mapped:
            tot_exec_t=0
            for task in scenario.constraint_graphs[graph].task_cluster[a].tasks:
                tot_exec_t+=scenario.graphs[graph].tasks[task].wcet[pe]
            if tot_exec_t > scenario.hyperperiod:
                scenario.constraint_graphs[graph].task_cluster[a].can_be_mapped.remove(pe)
                #print(pe + " removed")

    #Making sure that the messages between the same PEs is ignored in the next ILP
    #Untested code bits here
    for arc in scenario.graphs[graph].arcs:
        task_from=scenario.graphs[graph].arcs[arc].task_from
        task_to=scenario.graphs[graph].arcs[arc].task_to
        #print(task_from+"->"+task_to)
        if scenario.constraint_graphs[graph].task_to_cluster[task_to] != scenario.constraint_graphs[graph].task_to_cluster[task_from]:
            scenario.constraint_graphs[graph].messages[arc]=Message()
            scenario.constraint_graphs[graph].messages[arc].cluster_to=scenario.constraint_graphs[graph].task_to_cluster[task_to]
            scenario.constraint_graphs[graph].messages[arc].cluster_from=scenario.constraint_graphs[graph].task_to_cluster[task_from]

    #add constraints to problem...
    is_feasible=True
    constraints_to_add=[]
    for a in scenario.constraint_graphs[graph].task_cluster:
        if scenario.constraint_graphs[graph].task_cluster[a].can_be_mapped==None or not scenario.constraint_graphs[graph].task_cluster[a].can_be_mapped:
            #the current cluster is no longer feasible

            is_feasible=False
            scenario.num_of_added_con+=1
            i=0
            l={}
            for task in scenario.constraint_graphs[graph].task_cluster[a].tasks:
                temp=f"{task}_{str(a)}"
                l[temp]=('+',1)
                i+=1
            scenario.constraint_graphs[graph].pbp_data["cluster"].constraints.append([l,i,'<='])
            print("INFEASIBLEs")
    #edit_ILP(output_file,constraints_to_add,None)
    return is_feasible

def clustering_pb(graph):
    global scenario
    num_of_con=0;
    cluster="cluster"
    i=1
    scenario.constraint_graphs[graph].pbp_data[cluster]=PB_data()

    #clustering tasks
    for task in scenario.graphs[graph].tasks:
        num_of_con+=1
        l={}
        for j in range(i):
            temp=f"{task}_{str(j)}"
            print(temp)
            l[temp]=('+',1)
        scenario.constraint_graphs[graph].pbp_data[cluster].constraints.append([l,1,'='])
        i+=1

    #additional constraints to reduce symmetry
    i=1
    for task in scenario.graphs[graph].tasks:
        num_of_con+=1
        l={}
        temp=f"{task}_{str(i-1)}"
        l[temp]=('+',int((len(scenario.graphs[graph].tasks))))
        j=0
        for t in scenario.graphs[graph].tasks:
            if (j)>=i:
                temp=f"{t}_{str(i-1)}"
                l[temp]=('-',1)
            j+=1
        scenario.constraint_graphs[graph].pbp_data[cluster].constraints.append([l,0,'>='])
        i+=1

    i=1
    for task in scenario.graphs[graph].tasks:
        for j in range(i):
            print((task+"_"+str(j)))
            scenario.constraint_graphs[graph].pbp_data[cluster].decision_strat.append(((task+"_"+str(j)),random.uniform(0,1),bool(random.randint(0,1))))
        i+=1

def withdvfs_pb(graph,num_levels):
    global scenario
    num_of_con=0;
    line=""
    res_type="resource_alloc"
    i=1
    scenario.constraint_graphs[graph].pbp_data[res_type]=PB_data()

    i=1
    for cluster in scenario.constraint_graphs[graph].task_cluster:
        num_of_con+=1
        l={}
        for pe in scenario.constraint_graphs[graph].task_cluster[cluster].can_be_mapped:
            temp=f"{pe}_{cluster}"
            l[temp]=('+',1)
        scenario.constraint_graphs[graph].pbp_data[res_type].constraints.append([l,1,'='])
    if num_levels == None or num_levels < 3:
        print("No dvfs assumed")
    else:
        for cluster in scenario.constraint_graphs[graph].task_cluster:
            for task in scenario.constraint_graphs[graph].task_cluster[res_type].tasks:
                l={}
                num_of_con+=1
                for d in range(num_levels):
                    temp=f"{task}_{d}"
                    l[temp]=('+',1)
                scenario.constraint_graphs[graph].pbp_data[res_type].constraints.append([l,1,'='])
        #Declare the variables as binary
    num_var=0
    i=1
    for cluster in scenario.constraint_graphs[graph].task_cluster:
        for pe in scenario.constraint_graphs[graph].task_cluster[cluster].can_be_mapped:
            scenario.constraint_graphs[graph].pbp_data[res_type].decision_strat.append(((f"{pe}_{cluster}"),random.uniform(0,1),bool(random.randint(0,1))))
    if num_levels == None or num_levels < 3:
        print("No dvfs assumed")
    else:
        for cluster in scenario.constraint_graphs[graph].task_cluster:
            for task in scenario.constraint_graphs[graph].task_cluster[res_type].tasks:
                for d in range(num_levels):
                    scenario.constraint_graphs[graph].pbp_data[res_type].decision_strat.append(((f"{task}_{d}"),random.uniform(0,1),bool(random.randint(0,1))))
    print(f"ILP resource mapping written for graph")

def process_withdvfs(graph,num_levels):
    global scenario
    dvfs_levels = []
    if num_levels == None or num_levels < 3:
        dvfs_levels = [1]
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
            dvfs_levels.append(f_down+(i*step_size))
    #this creates a list of size dvfs_num_levels
    #the contents of this list will range from [1600/500 to 200/500]
    #now dvfs_level*freq=dvfs_mode_frequency and dvfs_level*volt=dvfs_mode_voltage
    for var in scenario.constraint_graphs[graph].pbp_data["resource_alloc"].assignment:
        more_vals=var.rsplit("_",1)
        if more_vals[0] in scenario.tables:
            scenario.constraint_graphs[graph].task_cluster[int(more_vals[1])].mapped_to=more_vals[0]
        else:
            scenario.constraint_graphs[graph].dvfs_level[more_vals[0]]=int(more_vals[1])

#ILP for assigning the Resource type to cluster and the dvfs mode to each task.

def dpll_solver(decision_strat,constraints,literal):
    for con in constraints:
        if not bool(con[0]) and con[1]==0 and con[2]=='=':
            constraints.remove(con)
        elif not bool(con[0]) and con[1]>=0 and con[2]=='<=':
            constraints.remove(con)
        elif not bool(con[0]) and con[1]<=0 and con[2]=='>=':
            print(con)
            constraints.remove(con)
        elif not bool(con[0]):
            return False, None
    assignment={}
    if len(constraints) == 0:
        return True, assignment
    if literal==len(decision_strat):
        #for con in constraints:
            #if not bool(con[0]):
                #print(con)
        return False,None
    cur_var = decision_strat[literal][0]
    var_val = decision_strat[literal][2]

    new_cons = deepcopy(constraints)
    for con in new_cons:
        if cur_var in con[0]:
            if con[0][cur_var][0]=='+':
                con[1]-=(con[0][cur_var][1]*int(var_val))
            else:
                con[1]+=(con[0][cur_var][1]*int(var_val))
            del con[0][cur_var]

    isAssigned, vals = dpll_solver(decision_strat,new_cons,(literal+1))
    if isAssigned:
        vals[cur_var]=var_val
        return True, vals

    var_val = not var_val
    new_cons = deepcopy(constraints)
    for con in new_cons:
        if cur_var in con[0]:
            if con[0][cur_var][0]=='+':
                con[1]-=(con[0][cur_var][1]*int(var_val))
            else:
                con[1]+=(con[0][cur_var][1]*int(var_val))
            del con[0][cur_var]

    isAssigned, vals = dpll_solver(decision_strat,new_cons,(literal+1))
    if isAssigned:
        vals[cur_var]=var_val
        return True, vals
    return False, None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_tgff", help="*.tgff file to parse")
    parser.add_argument("--tg", help="*name of task_graph",default="TASK_GRAPH")
    parser.add_argument("--core", help="name of core/PE", default="CLIENT_PE")
    parser.add_argument("-d", "--dir",default="./lp_files", help="output directory")
    parser.add_argument("-o", "--out",action="store", dest="out", default="ilp.lp", help="output file")
    parser.add_argument("--dvfs_level","--dvfs",action="store", dest="dvfs_num_levels", type=int, default=None, help="The number of dvfs_levels possible for each processor")
    args = parser.parse_args()
    global scenario
    scenario = Complete_Scenario()
    with open(args.input_tgff) as input_file:
        for block in get_blocks(input_file):
            process_block(block,args.tg,args.core)
    generate_noc(8,8)
    populate_task_params()

    phase=0
    #Processing each graph seperately
    for graph in scenario.graphs:

        scenario.constraint_graphs[graph] = Constraint_graph()
        clustering_pb(graph)

        i=0
        while(i<10):
            isassigned,scenario.2[graph].pbp_data["cluster"].assignment=dpll_solver(scenario.constraint_graphs[graph].pbp_data["cluster"].decision_strat,scenario.constraint_graphs[graph].pbp_data["cluster"].constraints,0)
            if not isassigned:
                print("Clustering constraints broken, fix now")
            if not process_clustering(graph):
                i+=1
            else:
                break
        if i>9:
            print(f"No feasible solution for {graph}")
        # isassigned,scenario.constraint_graphs[graph].pbp_data["cluster"].assignment=dpll_solver(scenario.constraint_graphs[graph].pbp_data["cluster"].decision_strat,scenario.constraint_graphs[graph].pbp_data["cluster"].constraints,0)
        # if not isassigned:
        #     print("Clustering constraints broken, fix now")
        # process_clustering(graph)

        withdvfs_pb(graph,args.dvfs_num_levels)
        isassigned,scenario.constraint_graphs[graph].pbp_data["resource_alloc"].assignment=dpll_solver(scenario.constraint_graphs[graph].pbp_data["resource_alloc"].decision_strat,scenario.constraint_graphs[graph].pbp_data["resource_alloc"].constraints,0)
        for a in scenario.constraint_graphs[graph].pbp_data["resource_alloc"].assignment:
            print(a)
            print(scenario.constraint_graphs[graph].pbp_data["resource_alloc"].assignment[a])
        process_withdvfs(graph,args.dvfs_num_levels)

        # plot_app_graph(graph,phase,args.dir)
        # plot_constraint_graph(graph,phase,args.dir)

        phase+=1

if __name__ == '__main__':
    main()
