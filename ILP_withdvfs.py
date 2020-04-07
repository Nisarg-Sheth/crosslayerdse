import os
import sys
import re
import argparse
import random
import subprocess
from graphviz import Digraph
from deap import *
from old_source import *

scenario = None

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
        scenario.tables[core_name]=Table(core_name,block[1].strip('#'),block[2].strip('#'),block[4].strip('#'))
        for i in range(5, len(block)):
            if not block[i].startswith('#'):
                scenario.tables[core_name].add_row(block[i])
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
                        #adding the WCET on the PE for each task
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

def generate_ILP1(output_file, graph):
    global scenario
    num_of_con=0;
    con_val= "constraint"
    with open(output_file, 'w') as f:
        #randomize the ILP generation
        f.write("Maximize\n")
        i=1
        line = ""
        for task in graph.tasks:
            line += f"+ 1 {task}_{random.randint(0,(i-1))} "
            i+=1
        f.write(f"problem: {line}\n")
        f.write("Subject To"+"\n")
        i=1
        #This represents the equation $summation_(t_i<J)(t_i) = 1
        for task in graph.tasks:
            num_of_con+=1
            con = f"{con_val}_{str(num_of_con)} : "
            line=" "
            for j in range(i):
                line += f" + 1 {task}_{str(j)} "
            line += " = 1"
            f.write(con+line+"\n")
            i+=1

        #The following equations are for ensuring the number of constraints can be controlled by the heuristic.
        i=1
        for task in graph.tasks:
            num_of_con+=1
            con = f"{con_val}_{str(num_of_con)} : "
            line=f"- 1 {task}_iscluster "
            j=0
            for t in graph.tasks:
                if (j+1)>=i:
                    line +=f"+ 1 {t}_{str(i-1)} "
                j+=1
            line += " >= 0"
            f.write(con+line+"\n")
            i+=1

        #Declare the variables as binary
        f.write("\n")
        f.write("Binary"+"\n\n")
        num_var=0
        i=1

        #the clustering variables
        for task in graph.tasks:
            for j in range(i):
                f.write(task+"_"+str(j)+"\n")
                num_var+=1
            i+=1

        # is clustered variables
        for task in graph.tasks:
            f.write(f"{task}_iscluster\n")


    print(f"ILP clustering written for graph")

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
    populate_task_params()

    phase=0
    #Processing each graph seperately
    for graph in scenario.graphs:
        out_name=args.out
        ext_id = out_name.rfind(".")
        prefix = out_name[:ext_id]
        ext = out_name[ext_id+1:]
        out_name = "%s_%d.%s" % (prefix, phase, ext)
        out_name1 = "%scluster_%d.%s" % (prefix, phase, ext)
        out_name2 = "%sresmap_%d.%s" % (prefix, phase, ext)
        out_name3 = "%sdvfs_%d.%s" % (prefix, phase, ext)
        result_file_name="%s_%d.%s" % ("result", phase, "sol")
        output_file_path=os.path.join(args.dir,out_name)
        result_file_path=os.path.join(args.dir,result_file_name)
        result_arg = "ResultFile="+result_file_path

        #The old 0-1 ILP formulation
        # generate_ILP(output_file_path,scenario.graphs[graph])
        # gurobi_run=subprocess.run(["gurobi_cl",result_arg,output_file_path], capture_output=True)
        # if "Optimal solution found" not in str(gurobi_run.stdout):
        #     print("THE SOLVER COULD NOT FIND A FEASIBLE SOLUTION, CHANGE CONSTRAINTS")
        #     break;
        # generate_con_graph(result_file_path,graph)
        # plot_constraint_graph(graph,phase,args.dir)

        #Task clustering ILP formation and processing
        generate_ILP1(os.path.join(args.dir,out_name1),scenario.graphs[graph])
        i=0
        while i<=100:
            #running gurobi on the output
            gurobi_run=subprocess.run(["gurobi_cl",result_arg,os.path.join(args.dir,out_name1)], capture_output=True)
            if "solution found" not in str(gurobi_run.stdout):
                print("THE SOLVER COULD NOT FIND A FEASIBLE SOLUTION, CHANGE CONSTRAINTS")
                print(str(gurobi_run.stdout))
                i=100
                break
            #this processing can be used to reduce the Design space. It also readies for the next ILP
            cluster_done=process_ILP1(result_file_path,os.path.join(args.dir,out_name1),graph)
            if cluster_done:
                break
            i+=1
        if i>=100:
            print("CLUSTERING FAILED")
            phase+=1
            continue
        #resource mapping ILP methodology.
        # generate_ILP2(os.path.join(args.dir,out_name2),graph)
        # #running gurobi on the output
        # gurobi_run=subprocess.run(["gurobi_cl",result_arg,os.path.join(args.dir,out_name2)], capture_output=True)
        # if "solution found" not in str(gurobi_run.stdout):
        #     print("THE SOLVER COULD NOT FIND A FEASIBLE SOLUTION, CHANGE CONSTRAINTS")
        #     break;
        # #this processing can be used to reduce the Design space.
        # process_ILP2(result_file_path,os.path.join(args.dir,out_name2),graph)
        #
        # #dvfs_level ILP methodology.
        # if args.dvfs_num_levels!=None:
        #     generate_ILP3(os.path.join(args.dir,out_name3),graph,args.dvfs_num_levels)
        #     #running gurobi on the output
        #     gurobi_run=subprocess.run(["gurobi_cl",result_arg,os.path.join(args.dir,out_name3)], capture_output=True)
        #     if "solution found" not in str(gurobi_run.stdout):
        #         print("THE SOLVER COULD NOT FIND A FEASIBLE SOLUTION, CHANGE CONSTRAINTS")
        #         break;
        #     phase+=1
        #     #this processing can be used to reduce the Design space.
        #     process_ILP3(result_file_path,os.path.join(args.dir,out_name3),graph,args.dvfs_num_levels)
        #
        generate_ILP_withdvfs(os.path.join(args.dir,out_name2),graph,args.dvfs_num_levels)
        #running gurobi on the output
        gurobi_run=subprocess.run(["gurobi_cl",result_arg,os.path.join(args.dir,out_name2)], capture_output=True)
        if "solution found" not in str(gurobi_run.stdout):
            print("THE SOLVER COULD NOT FIND A FEASIBLE SOLUTION, CHANGE CONSTRAINTS")
            print(str(gurobi_run.stdout))
            break;
        #this processing can be used to reduce the Design space. It also readies for the next ILP
        process_ILP_withdvfs(result_file_path,os.path.join(args.dir,out_name2),graph,args.dvfs_num_levels)

        plot_app_graph(graph,phase,args.dir)
        plot_constraint_graph(graph,phase,args.dir)

        phase+=1

if __name__ == '__main__':
    main()