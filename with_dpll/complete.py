import os
import sys
import re
import argparse
import random
import subprocess
from graphviz import Digraph
from deap import base
from deap import creator
from deap import tools
from source import *
from copy import deepcopy


scenario = None
random.seed(622)

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
                        #adding the WCET on the PE for each task
                        scenario.graphs[graph].tasks[task].wcet[table]=float(scenario.tables[table].values[type_of_task][3])
                        #adding the task_power on the PE to the task arc_details
                        scenario.graphs[graph].tasks[task].power[table]=float(scenario.tables[table].values[type_of_task][6])
                        #adding code bits to the task details
                        scenario.graphs[graph].tasks[task].code_bits[table]=float(scenario.tables[table].values[type_of_task][5])
                        #adding preemeption_time
                        scenario.graphs[graph].tasks[task].preempt_time[table]=float(scenario.tables[table].values[type_of_task][4])

        for task in scenario.graphs[graph].tasks:
            for arc in scenario.graphs[graph].arcs:
                task_to=scenario.graphs[graph].arcs[arc].task_to
                task_from=(scenario.graphs[graph].arcs[arc].task_from)
                if scenario.graphs[graph].tasks[task_to].priority<(scenario.graphs[graph].tasks[task_from].priority+1):
                    scenario.graphs[graph].tasks[task_to].priority=(scenario.graphs[graph].tasks[task_from].priority+1)

def generate_noc(length,breadth):
    global scenario
    # for temp in scenario.all_tables:
    #     scenario.tables[temp]=scenario.all_tables[temp]
    for i in range(length):
        l=[]
        for j in range(breadth):
            temp=random.sample(scenario.all_tables.keys(),1)
            scenario.tables[temp[0]]=scenario.all_tables[temp[0]]
            l.append(temp[0])
        scenario.NOC.append(l)

def gen_compl_pb(con_graph,graph):
    global scenario
    complete="complete"
    i=0
    num_of_con=0
    num_of_vars=0
    con_graph.pbp_data[complete]=PB_data()
    map_list=[]
    for task in scenario.graphs[graph].tasks:
        map_list.append(scenario.graphs[graph].tasks[task].pe_list)
    for task in scenario.graphs[graph].tasks:
        l={}
        # Tslave+ Tmaster = 1
        temp=f"{task}_master"
        con_graph.pbp_data[complete].decision_strat[temp]=[random.uniform(0,1),bool(random.randint(0,1))]
        l[temp]=('+',1)
        temp=f"{task}_slave"
        con_graph.pbp_data[complete].decision_strat[temp]=[random.uniform(0,1),bool(random.randint(0,1))]
        l[temp]=('+',1)
        con_graph.pbp_data[complete].constraints.append([l,1,'='])


def gen_comp_pb(con_graph,graph):
    global scenario
    complete="complete"
    i=0
    num_of_con=0
    num_of_vars=0
    con_graph.pbp_data[complete]=PB_data()
    map_list=[]
    for task in scenario.graphs[graph].tasks:
        map_list.append(scenario.graphs[graph].tasks[task].pe_list)
    for task in scenario.graphs[graph].tasks:
        l={}
        # Tslave+ Tmaster = 1
        temp=f"{task}_master"
        con_graph.pbp_data[complete].decision_strat[temp]=[random.uniform(0,1),bool(random.randint(0,1))]
        l[temp]=('+',1)
        temp=f"{task}_slave"
        con_graph.pbp_data[complete].decision_strat[temp]=[random.uniform(0,1),bool(random.randint(0,1))]
        l[temp]=('+',1)
        con_graph.pbp_data[complete].constraints.append([l,1,'='])
        # Connnected in Vertical direction,
        # Connected in Horizontal direction,
        # Is slave only connected to one??
        l1={}
        temp=f"{task}_master"
        if (i>0):
            l1[temp]=('+',i)
        l2={}
        temp=f"{task}_slave"
        if ((scenario.graphs[graph].num_of_tasks-(i+1))>0):
            l2[temp]=('+',(scenario.graphs[graph].num_of_tasks-(i+1)))
        l3={}
        temp=f"{task}_slave"
        l3[temp]=('-',1)
        j=0
        for task1 in scenario.graphs[graph].tasks:
            if task!=task1:
                temp=f"C_{task1}_{task}"
                con_graph.pbp_data[complete].decision_strat[temp]=[random.uniform(0,1),bool(random.randint(0,1))]
                l2[temp]=('+',1)
            if j<i:
                temp=f"C_{task}_{task1}"
                l1[temp]=('+',1)
                l3[temp]=('+',1)
            elif j>i:
                temp=f"C_{task1}_{task}"
            j+=1
        print(l1,l2,l3)
        con_graph.pbp_data[complete].constraints.append([l1,i,'<='])
        con_graph.pbp_data[complete].constraints.append([l2,(scenario.graphs[graph].num_of_tasks-(i+1)),'<='])
        con_graph.pbp_data[complete].constraints.append([l3,0,'='])

        #Mapping the Tmasters to Resources
        l4={}
        temp=f"{task}_master"
        l4[temp]=('-',1)
        for map in map_list[i]:
            temp=f"map_{task}_{map}"
            con_graph.pbp_data[complete].decision_strat[temp]=[random.uniform(0,1),bool(random.randint(0,1))]
            l4[temp]=('+',1)
        con_graph.pbp_data[complete].constraints.append([l4,0,'='])

        #DVFS Level assignment
        if scenario.dvfs!=None and scenario.dvfs>=3:
            l4={}
            temp=f"{task}_master"
            l4[temp]=('-',1)
            for level in range(scenario.dvfs):
                temp=f"dvfs_{level}_{task}"
                con_graph.pbp_data[complete].decision_strat[temp]=[random.uniform(0,1),bool(random.randint(0,1))]
                l4[temp]=('+',1)
            con_graph.pbp_data[complete].constraints.append([l4,0,'='])
        #verifying that mapping is not bad.
        j=0
        for task1 in scenario.graphs[graph].tasks:
            # if j<i:
            #     temp=f"C_{task}_{task1}"
            #     l5={}
            #     l5[temp]=('-',1)
            #     for pe in map_list[i]:
            #         if pe in map_list[j]:
            #             temp=f"map_{task1}_{pe}"
            #             l5[temp]=('+',1)
            #     con_graph.pbp_data[complete].constraints.append([l5,0,'>='])
            if j>i:
                l6={}
                temp=f"C_{task1}_{task}"
                l6[temp]=('-',1)
                for pe in map_list[i]:
                    if pe in map_list[j]:
                        temp=f"map_{task}_{pe}"
                        l6[temp]=('+',1)
                con_graph.pbp_data[complete].constraints.append([l6,0,'>='])
            j+=1
        i+=1

    # for m in scenario.graphs[graph].arcs:
    #     #assign service level
    #     l1={}
    #     for j in range(scenario.service_level):
    #         l1[f"sl_{j}_{m}"]=('+',1)
    #         con_graph.pbp_data[complete].decision_strat[f"sl_{j}_{m}"]=[random.uniform(0,1),bool(random.randint(0,1))]
    #     con_graph.pbp_data[complete].constraints.append([l1,1,'='])
    #     #assign hop distance
    #     l2={}
    #     for j in range(scenario.max_hop):
    #         l2[f"hop_{j}_{m}"]=('+',1)
    #         con_graph.pbp_data[complete].decision_strat[f"hop_{j}_{m}"]=[random.uniform(0,1),bool(random.randint(0,1))]
    #     con_graph.pbp_data[complete].constraints.append([l2,1,'='])


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
            print(parts)
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

#feasibilty of constraint on the physical NOC
def feasiblity_con_graph(con_graph,graph):
    global scenario

#Plotting the constraint graph
def plot_constraint_graph(con_graph,graph,phase,dir):
    constraint_g = Digraph(comment = graph, format='png')
    for task in con_graph.task_cluster:
        to_show=""
        mapped_to = con_graph.task_cluster[task].mapped_to
        for a in con_graph.task_cluster[task].tasks:
            to_show+=f"{a}(dvfs_level {con_graph.dvfs_level[a]}), "
        to_show= f"[{to_show}]\n"+mapped_to
        constraint_g.node(str(task),label=to_show)
    for m in con_graph.messages:
        to_show="m"
        to_show=to_show + "\n"+str(con_graph.messages[m].sl)
        to_show=to_show + "\n"+str(con_graph.messages[m].hop)
        constraint_g.node(m,label=to_show)
        constraint_g.edge(str(con_graph.messages[m].cluster_from), m)
        constraint_g.edge(m,str(con_graph.messages[m].cluster_to))
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

def process_clustering(graph):
    global scenario
    for var in scenario.constraint_graphs[graph].pbp_data["cluster"].assignment:
        if scenario.constraint_graphs[graph].pbp_data["cluster"].assignment[var]==1:
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
        l[temp]=('+',(len(scenario.graphs[graph].tasks)))
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
        #assign dvfs level to each task
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
def messaging_pb(graph):
    global scenario
    num_of_con=0;
    message="message"
    i=1
    scenario.constraint_graphs[graph].pbp_data[message]=PB_data()

    #clustering tasks
    for task in scenario.graphs[graph].tasks:
        num_of_con+=1
        l={}
        for j in range(i):
            temp=f"{task}_{str(j)}"
            print(temp)
            l[temp]=('+',1)
        scenario.constraint_graphs[graph].pbp_data[message].constraints.append([l,1,'='])
        i+=1

def dpll_solver(decision_strat,constraints,literal):
    #print(literal)
    elem_del=[]
    var_list=[]
    var_dets=[]
    cur_var = None
    assignment={}
    for con in constraints:
        if con[1]==0 and con[2]=='=':
            temp_vars=[]
            #append the variables that will inevitably be zero
            for a in con[0]:
                if con[0][a][0]!='+':
                    temp_vars=[]
                    break
                temp_vars.append(a)
            #delete those variables from constraints outright as they will be zero
            for vars in temp_vars:
                for cons in constraints:
                    if vars in cons[0]:
                        del cons[0][vars]
            #Remove the variables from the decision_strat
            for vars in temp_vars:
                var_dets.append(decision_strat[vars])
                var_list.append(vars)
                decision_strat[vars][0]=-1
        elif con[1]<=0 and con[2]=='<=':
            temp_vars=[]
            #append the variables that will inevitably be zero
            for a in con[0]:
                if con[0][a][0]!='+':
                    temp_vars=[]
                    break
                temp_vars.append(a)
            #delete those variables from constraints outright as they will be zero
            for vars in temp_vars:
                for cons in constraints:
                    if vars in cons[0]:
                        del cons[0][vars]
            #Remove the variables from the decision_strat
            for vars in temp_vars:
                var_dets.append(decision_strat[vars])
                var_list.append(vars)
                decision_strat[vars][0]=-1


    #find a variable to assign value, else return false
    for vars in decision_strat:
        if decision_strat[vars][0]!=(-1):
            cur_var=vars
            var_val = decision_strat[cur_var][1]
            var_priority= decision_strat[cur_var][0]
            decision_strat[cur_var][0]=-1
            break
    l="-"
    for i in range(literal):
        l+="-"
    #print(l+cur_var)

    for con in constraints:
        if not bool(con[0]) and con[1]>=0 and con[2]=='<=':
            elem_del.append(con)
        elif not bool(con[0]) and con[1]<=0 and con[2]=='>=':
            elem_del.append(con)
        elif not bool(con[0]) and con[1]==0 and con[2]=='=':
            elem_del.append(con)
        elif not bool(con[0]):
            print(con[1])
            #print(con[2])
            for i in range(len(var_list)):
                decision_strat[var_list[i]]=var_dets[i]
                #print("rhis is"+var_list[i])
            if cur_var!=None:
                decision_strat[cur_var]=[var_priority,var_val]
            return False, None
    for e in elem_del:
        constraints.remove(e)
    if len(constraints) == 0:
        #print("valid solution to PBP found")
        for i in range(len(var_list)):
            decision_strat[var_list[i]]=var_dets[i]
        if cur_var!=None:
            decision_strat[cur_var]=[var_priority,var_val]
        return True, assignment

    if cur_var!=None:
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
            for i in range(len(var_list)):
                decision_strat[var_list[i]]=var_dets[i]
            decision_strat[cur_var]=[var_priority,var_val]
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
            for i in range(len(var_list)):
                decision_strat[var_list[i]]=var_dets[i]
            decision_strat[cur_var]=[var_priority,var_val]
            return True, vals

    for i in range(len(var_list)):
        decision_strat[var_list[i]]=var_dets[i]
    if cur_var!=None:
        decision_strat[cur_var]=[var_priority,var_val]
    return False, None
#Changed solver
def dll_solver(decision_strat,constraints,literal):
    #print(literal)
    elem_del=[]
    var_list=[]
    var_dets=[]
    cur_var = None
    assignment={}
    for con in constraints:
        if con[1]==0 and con[2]=='=':
            temp_vars=[]
            for a in con[0]:
                if con[0][a][0]!='+':
                    temp_vars=[]
                    break
                temp_vars.append(a)
            for vars in temp_vars:
                for cons in constraints:
                    if vars in cons[0]:
                        del cons[0][vars]
            for vars in temp_vars:
                var_dets.append(decision_strat[vars])
                var_list.append(vars)
                decision_strat[vars][0]=-1
        elif con[1]==0 and con[2]=='<=':
            temp_vars=[]
            for a in con[0]:
                if con[0][a][0]!='+':
                    temp_vars=[]
                    break
                temp_vars.append(a)
            for vars in temp_vars:
                for cons in constraints:
                    if vars in cons[0]:
                        del cons[0][vars]
            for vars in temp_vars:
                var_dets.append(decision_strat[vars])
                var_list.append(vars)
                decision_strat[vars][0]=-1

    for vars in decision_strat:
        if decision_strat[vars][0]!=(-1):
            cur_var=vars
            var_val = decision_strat[cur_var][1]
            var_priority= decision_strat[cur_var][0]
            decision_strat[cur_var][0]=-1
            break
    if cur_var==None:
        for i in range(len(var_list)):
            decision_strat[var_list[i]]=var_dets[i]
        return False,None
    l="-"
    for i in range(literal):
        l+="-"
    print(l+cur_var)
    # for key,value in decision_strat.items():
    #     cur_var = key
    #     var_val = value[1]
    #     var_priority=value[0]
    #     decision_strat.pop(cur_var)
    #     break
    for con in constraints:
        if not bool(con[0]) and con[1]>=0 and con[2]=='<=':
            elem_del.append(con)
        elif not bool(con[0]) and con[1]<=0 and con[2]=='>=':
            elem_del.append(con)
        elif not bool(con[0]) and con[1]==0 and con[2]=='=':
            elem_del.append(con)
        elif not bool(con[0]):
            print(con[1])
            print(con[2])
            for i in range(len(var_list)):
                decision_strat[var_list[i]]=var_dets[i]
                print("rhis is"+var_list[i])
            if cur_var!=None:
                decision_strat[cur_var]=[var_priority,var_val]
            return False, None
    for e in elem_del:
        constraints.remove(e)
    if len(constraints) == 0:
        #print("valid solution to PBP found")
        for i in range(len(var_list)):
            decision_strat[var_list[i]]=var_dets[i]
        if cur_var!=None:
            decision_strat[cur_var]=[var_priority,var_val]
        return True, assignment

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
        for i in range(len(var_list)):
            decision_strat[var_list[i]]=var_dets[i]
        decision_strat[cur_var]=[var_priority,var_val]
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
        for i in range(len(var_list)):
            decision_strat[var_list[i]]=var_dets[i]
        decision_strat[cur_var]=[var_priority,var_val]
        return True, vals

    for i in range(len(var_list)):
        decision_strat[var_list[i]]=var_dets[i]
    decision_strat[cur_var]=[var_priority,var_val]
    return False, None

def process_pbp_data(con_graph):
    #sort decision strat by the increasing order of decision priority
    decision_strat=OrderedDict(deepcopy(sorted(con_graph.pbp_data["complete"].decision_strat.items() , key=lambda x : -x[1][0])))
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

    for con in con_graph.pbp_data["complete"].constraints:
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
    isAssigned, assignment= pbs_solver(decision_strat,con_graph.pbp_data["complete"].constraints,con_dets,var_list)
    # for val in decision_strat:
    #     if val in assignment:
    #         if "idct" in val:
    #             print(assignment[val])
    #             print(val)
    #     else:
    #         print("MISSED OUT ON VARS")
    if isAssigned==False:
        print("Assignment was not successful")
        return None
    return assignment

def pbs_solver(decision_strat,constraints,con_dets,variables):
    cur_var = None
    var_val = None
    assignment={}
    var_list={}
    infeasible_con_list=[]
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
                    infeasible_con_list.append(i)
            #add value of coefficient to current sum of constraint
            con_dets[i][1]+=variables[cur_var][0][i]
        else:
            #Make sure that assigning the value does not cause conflict
            if con_dets[i][0]!='<=':
                if (con_dets[i][2]-variables[cur_var][0][i])<con_dets[i][3]:
                    isFeasible=False
                    infeasible_con_list.append(i)
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
                                infeasible_con_list.append(i)
                        var_list[vars]=False
                    elif constraints[i][0][vars][0]=='-' and (con_dets[i][1]+variables[vars][1][i])>con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=True:
                                isFeasible=False
                                infeasible_con_list.append(i)
                        var_list[vars]=True
                elif con_dets[i][0]!='<=':
                    #if the coefficient of vars is necessary, make sure it is true
                    if constraints[i][0][vars][0]=='+' and (con_dets[i][2]-variables[vars][0][i])<con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=False:
                                isFeasible=False
                                infeasible_con_list.append(i)
                        var_list[vars]=False
                        #print("THIS",vars)
                    #if the sign of vars is negative in the constraint, then make sure it is false.
                    elif constraints[i][0][vars][0]=='-' and (con_dets[i][2]-variables[vars][1][i])<con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=True:
                                isFeasible=False
                                infeasible_con_list.append(i)
                        var_list[vars]=True

    for i in variables[cur_var][1]:
        #update the constraints list based on the value of the current variable.
        if var_val==0:
            #make sure that it is feasible for the constraint to be assigned true or false.
            if con_dets[i][0]!='>=':
                #if current sum + coefficient>objective goal of constraint and coefficient is positive
                if (con_dets[i][1]+variables[cur_var][1][i])>con_dets[i][3]:
                    isFeasible=False
                    infeasible_con_list.append(i)
            con_dets[i][1]+=variables[cur_var][1][i]
        else:
            #Make sure that assigning the value does not cause conflict
            if con_dets[i][0]!='<=':
                if (con_dets[i][2]-variables[cur_var][1][i])<con_dets[i][3]:
                    isFeasible=False
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
                        var_list[vars]=False
                    elif constraints[i][0][vars][0]=='-' and (con_dets[i][1]+variables[vars][1][i])>con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=True:
                                isFeasible=False
                        var_list[vars]=True
                elif con_dets[i][0]!='<=':
                    if constraints[i][0][vars][0]=='+' and (con_dets[i][2]-variables[vars][0][i])<con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=False:
                                isFeasible=False
                        var_list[vars]=False
                    elif constraints[i][0][vars][0]=='-' and (con_dets[i][2]-variables[vars][1][i])<con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=True:
                                isFeasible=False
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
                #add value of coefficient to current sum of constraint
                con_dets[i][1]+=variables[val][0][i]
            else:
                #subtract value of coefficient from maximum posible sum of constraints
                #Make sure that assigning the value does not cause conflict
                if con_dets[i][0]!='<=':
                    if (con_dets[i][2]-variables[val][0][i])<con_dets[i][3]:
                                isFeasible=False
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
                #add value of coefficient to current sum of constraint
                con_dets[i][1]+=variables[val][1][i]
            else:

                #Make sure that assigning the value does not cause conflict
                if con_dets[i][0]!='<=':
                    if (con_dets[i][2]-variables[val][1][i])<con_dets[i][3]:
                                isFeasible=False
                #subtract value of coefficient from maximum posible sum of constraints
                con_dets[i][2]-=variables[val][1][i]

    #after assigning the values of the assignment, lets check if the whole situation is feasible.
    reprocess=False
    val_return=cur_var
    if isFeasible==True:
        #print("____NEXT LEVEL___")
        isAssigned, vals= pbs_solver(decision_strat,constraints,con_dets,variables)
        if isAssigned:
            vals[cur_var]=var_val
            for val in var_list:
                vals[val]=var_list[val]
            return True, vals
        else:
            reprocess=False
            val_return=vals
            for i in variables[cur_var][0]:
                if vals in constraints[i][0].keys():
                    print(constraints[i][0])
                    reprocess=False
            for i in variables[cur_var][1]:
                if vals in constraints[i][0].keys():
                    print(constraints[i][0])
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
        decision_strat[cur_var][0]=1
        return False,val_return

    #Change the value if it is infeasible, repeat.
    var_val=not var_val
    #print(f"Swap decision variable for {cur_var}")
    #print("The current value is ",cur_var,var_val)


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
            #add value of coefficient to current sum of constraint
            con_dets[i][1]+=variables[cur_var][0][i]
        else:
            #Make sure that assigning the value does not cause conflict
            if con_dets[i][0]!='<=':
                if (con_dets[i][2]-variables[cur_var][0][i])<con_dets[i][3]:
                    isFeasible=False
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
                        var_list[vars]=False
                    elif constraints[i][0][vars][0]=='-' and (con_dets[i][1]+variables[vars][1][i])>con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=True:
                                isFeasible=False
                        var_list[vars]=True
                elif con_dets[i][0]!='<=':
                    #if the coefficient of vars is necessary, make sure it is true
                    if constraints[i][0][vars][0]=='+' and (con_dets[i][2]-variables[vars][0][i])<con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=False:
                                isFeasible=False
                        var_list[vars]=False
                        #print("THIS",vars)
                    #if the sign of vars is negative in the constraint, then make sure it is false.
                    elif constraints[i][0][vars][0]=='-' and (con_dets[i][2]-variables[vars][1][i])<con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=True:
                                isFeasible=False
                        var_list[vars]=True

    for i in variables[cur_var][1]:
        #update the constraints list based on the value of the current variable.
        if var_val==0:
            #make sure that it is feasible for the constraint to be assigned true or false.
            if con_dets[i][0]!='>=':
                #if current sum + coefficient>objective goal of constraint and coefficient is positive
                if (con_dets[i][1]+variables[cur_var][1][i])>con_dets[i][3]:
                    isFeasible=False
            con_dets[i][1]+=variables[cur_var][1][i]
        else:
            #Make sure that assigning the value does not cause conflict
            if con_dets[i][0]!='<=':
                if (con_dets[i][2]-variables[cur_var][1][i])<con_dets[i][3]:
                    isFeasible=False
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
                        var_list[vars]=False
                    elif constraints[i][0][vars][0]=='-' and (con_dets[i][1]+variables[vars][1][i])>con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=True:
                                isFeasible=False
                        var_list[vars]=True
                elif con_dets[i][0]!='<=':
                    if constraints[i][0][vars][0]=='+' and (con_dets[i][2]-variables[vars][0][i])<con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=False:
                                isFeasible=False
                        var_list[vars]=False
                    elif constraints[i][0][vars][0]=='-' and (con_dets[i][2]-variables[vars][1][i])<con_dets[i][3]:
                        if vars in var_list:
                            if var_list[vars]!=True:
                                isFeasible=False
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
                #add value of coefficient to current sum of constraint
                con_dets[i][1]+=variables[val][0][i]
            else:
                #subtract value of coefficient from maximum posible sum of constraints
                #Make sure that assigning the value does not cause conflict
                if con_dets[i][0]!='<=':
                    if (con_dets[i][2]-variables[val][0][i])<con_dets[i][3]:
                                isFeasible=False
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
                #add value of coefficient to current sum of constraint
                con_dets[i][1]+=variables[val][1][i]
            else:

                #Make sure that assigning the value does not cause conflict
                if con_dets[i][0]!='<=':
                    if (con_dets[i][2]-variables[val][1][i])<con_dets[i][3]:
                                isFeasible=False
                #subtract value of coefficient from maximum posible sum of constraints
                con_dets[i][2]-=variables[val][1][i]

    #after assigning the values of the assignment, lets check if the whole situation is feasible.
    val_return=cur_var
    if isFeasible==True:
        #print("____NEXT LEVEL___")
        isAssigned, vals= pbs_solver(decision_strat,constraints,con_dets,variables)
        if isAssigned:
            vals[cur_var]=var_val
            for val in var_list:
                vals[val]=var_list[val]
            return True, vals
        else:
            val_return=vals
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
    return False,val_return

def clustering_pb1(graph,con_graph):
    global scenario
    num_of_con=0;
    cluster="cluster"
    i=1
    con_graph.pbp_data[cluster]=PB_data()

    #clustering tasks
    for task in scenario.graphs[graph].tasks:
        num_of_con+=1
        l={}
        for j in range(i):
            temp=f"{task}_{str(j)}"
            #print(temp)
            l[temp]=('+',1)
        con_graph.pbp_data[cluster].constraints.append([l,1,'='])
        i+=1

    #additional constraints to reduce symmetry
    i=1
    for task in scenario.graphs[graph].tasks:
        num_of_con+=1
        l={}
        temp=f"{task}_{str(i-1)}"
        l[temp]=('+',(len(scenario.graphs[graph].tasks)))
        j=0
        for t in scenario.graphs[graph].tasks:
            if (j)>=i:
                temp=f"{t}_{str(i-1)}"
                l[temp]=('-',1)
            j+=1
        con_graph.pbp_data[cluster].constraints.append([l,0,'>='])
        i+=1

    i=1

    for task in scenario.graphs[graph].tasks:
        for j in range(i):
            con_graph.pbp_data[cluster].decision_strat[(f"{task}_{str(j)}")]=[random.uniform(0,1),bool(random.randint(0,1))]
        i+=1
def withdvfs_pb1(graph,con_graph,num_levels):
    global scenario
    num_of_con=0;
    line=""
    res_type="resource_alloc"
    i=1
    con_graph.pbp_data[res_type]=PB_data()

    i=1
    for cluster in con_graph.task_cluster:
        num_of_con+=1
        l={}
        for pe in con_graph.task_cluster[cluster].can_be_mapped:
            temp=f"{pe}_{cluster}"
            l[temp]=('+',1)
        con_graph.pbp_data[res_type].constraints.append([l,1,'='])
    if num_levels == None or num_levels < 3:
        print("No dvfs assumed")
    else:
        for cluster in con_graph.task_cluster:
            for task in con_graph.task_cluster[res_type].tasks:
                l={}
                num_of_con+=1
                for d in range(num_levels):
                    temp=f"{task}_{d}"
                    l[temp]=('+',1)
                con_graph.pbp_data[res_type].constraints.append([l,1,'='])
        #Declare the variables as binary
    num_var=0
    i=1
    for cluster in con_graph.task_cluster:
        for pe in con_graph.task_cluster[cluster].can_be_mapped:
            con_graph.pbp_data[res_type].decision_strat.append(((f"{pe}_{cluster}"),random.uniform(0,1),bool(random.randint(0,1))))
    if num_levels == None or num_levels < 3:
        print("No dvfs assumed")
    else:
        for cluster in con_graph.task_cluster:
            for task in con_graph.task_cluster[res_type].tasks:
                for d in range(num_levels):
                    con_graph.pbp_data[res_type].decision_strat.append(((f"{task}_{d}"),random.uniform(0,1),bool(random.randint(0,1))))
    print(f"ILP resource mapping written for graph")
def process_withdvfs1(graph,con_graph,num_levels):
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
    for var in con_graph.pbp_data["resource_alloc"].assignment:
        more_vals=var.rsplit("_",1)
        if more_vals[0] in scenario.tables:
            con_graph.task_cluster[int(more_vals[1])].mapped_to=more_vals[0]
        else:
            con_graph.dvfs_level[more_vals[0]]=int(more_vals[1])
def messaging_pb1(graph,con_graph):
    global scenario
    num_of_con=0;
    message="message"
    i=1
    con_graph.pbp_data[message]=PB_data()

    #clustering tasks
    for task in scenario.graphs[graph].tasks:
        num_of_con+=1
        l={}
        for j in range(i):
            temp=f"{task}_{str(j)}"
            print(temp)
            l[temp]=('+',1)
        con_graph.pbp_data[message].constraints.append([l,1,'='])
        i+=1
def process_clustering1(graph,con_graph):
    global scenario
    for var in con_graph.pbp_data["cluster"].assignment:
        a = var.rsplit("_",1)
        if int(a[1]) in con_graph.task_cluster:
            con_graph.task_cluster[int(a[1])].tasks.append(a[0])
            con_graph.task_to_cluster[a[0]]=int(a[1])
        else:
            con_graph.task_cluster[int(a[1])]=Task_cluster()
            con_graph.task_cluster[int(a[1])].tasks.append(a[0])
            con_graph.task_to_cluster[a[0]]=int(a[1])

    #Adding the possible PEs to each task cluster
    for a in con_graph.task_cluster:
        i=0
        pe_dict={}
        for task in con_graph.task_cluster[a].tasks:
            i+=1
            for pe in scenario.graphs[graph].tasks[task].pe_list:
                if pe in pe_dict:
                    pe_dict[pe]+=1
                else:
                    pe_dict[pe]=1
        for pe in pe_dict:
            if pe_dict[pe]==i:
                con_graph.task_cluster[a].can_be_mapped.append(pe)

        #Making sure we don't exceed the hyperperiod on the PE
        #this is an additional check
        for pe in con_graph.task_cluster[a].can_be_mapped:
            tot_exec_t=0
            for task in con_graph.task_cluster[a].tasks:
                tot_exec_t+=scenario.graphs[graph].tasks[task].wcet[pe]
            if tot_exec_t > scenario.hyperperiod:
                con_graph.task_cluster[a].can_be_mapped.remove(pe)
                #print(pe + " removed")

    #Making sure that the messages between the same PEs is ignored in the next ILP
    #Untested code bits here
    for arc in scenario.graphs[graph].arcs:
        task_from=scenario.graphs[graph].arcs[arc].task_from
        task_to=scenario.graphs[graph].arcs[arc].task_to
        #print(task_from+"->"+task_to)
        if con_graph.task_to_cluster[task_to] != con_graph.task_to_cluster[task_from]:
            con_graph.messages[arc]=Message()
            con_graph.messages[arc].cluster_to=con_graph.task_to_cluster[task_to]
            con_graph.messages[arc].cluster_from=con_graph.task_to_cluster[task_from]

    #add constraints to problem...
    is_feasible=True
    constraints_to_add=[]
    for a in con_graph.task_cluster:
        if con_graph.task_cluster[a].can_be_mapped==None or not con_graph.task_cluster[a].can_be_mapped:
            #the current cluster is no longer feasible

            is_feasible=False
            scenario.num_of_added_con+=1
            i=0
            l={}
            for task in con_graph.task_cluster[a].tasks:
                temp=f"{task}_{str(a)}"
                l[temp]=('+',1)
                i+=1
            con_graph.pbp_data["cluster"].constraints.append([l,i,'<='])
            print("INFEASIBLEs")
    #edit_ILP(output_file,constraints_to_add,None)
    return is_feasible

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
    scenario.dvfs_levels = []
    if num_levels == None or num_levels < 3:
        scenario.dvfs_levels = [1]
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
            scenario.dvfs_levels.append(f_down+(i*step_size))
    #this creates a list of size dvfs_num_levels
    #the contents of this list will range from [1600/500 to 200/500]
    #now dvfs_level*freq=dvfs_mode_frequency and dvfs_level*volt=dvfs_mode_voltage

def process_cons(con_graph):
    con_graph.pbp_data["complete"].assignment=process_pbp_data(con_graph)
    gen_comp_con_graph(con_graph,con_graph.graph)
    feasiblity_con_graph(con_graph,con_graph.graph)

def make_individual(name="la"):
    con_graph=creator.Individual()
    con_graph.graph=name
    gen_comp_pb(con_graph,name)
    con_graph.pbp_data["complete"].assignment=process_pbp_data(con_graph)
    # for ass in con_graph.pbp_data["complete"].assignment:
    #     if "pulse" in ass:
    #         print(ass)
    #         print(con_graph.pbp_data["complete"].assignment[ass])
    print("Individual")
    gen_comp_con_graph(con_graph,name)
    feasiblity_con_graph(con_graph,name)

    return con_graph

def makepop(graph_name="la", pop_size=5):
    l = []
    for i in range(pop_size):
        l.append(toolbox.individual(name=graph_name))
    return l

def evalParams(individual):
    global scenario
    graph=individual.graph
    energy=0
    task_list=[]
    task_start={}
    cluster_time={}

    dvfs_level=1
    message_communication_time=0.001
    #Computing the total energy usage
    for cluster in individual.task_cluster:
        cluster_time[cluster]=0
        if scenario.dvfs>1:
            dvfs_level=scenario.dvfs_level[(individual.dvfs_level[cluster])]
        for task in individual.task_cluster[cluster].tasks:
            mapped=individual.task_cluster[cluster].mapped_to
            wcet=scenario.graphs[graph].tasks[task].wcet[mapped]
            power=scenario.graphs[graph].tasks[task].power[mapped]
            energy+=(wcet*power*dvfs_level*dvfs_level)

    #Sorting tasks according to priority
    for task in scenario.graphs[graph].tasks:
        task_list.append([scenario.graphs[graph].tasks[task].priority,task])
        task_start[task]=0
    task_list.sort(key=lambda x: x[1])
    #setting lower limit on task start time
    for task_dets in task_list:
        task=task_dets[1]
        cluster=individual.task_to_cluster[task]
        mapped=individual.task_cluster[cluster].mapped_to
        cluster_time[cluster]=(task_start[task]+scenario.graphs[graph].tasks[task].wcet[mapped]*dvfs_level)
        for task1 in individual.task_cluster[cluster].tasks:
            if (scenario.graphs[graph].tasks[task1].priority>task_dets[0]):
                if (task_start[task1]<(task_start[task]+(scenario.graphs[graph].tasks[task].wcet[mapped]*dvfs_level))):
                    task_start[task1]=(task_start[task]+(scenario.graphs[graph].tasks[task].wcet[mapped]*dvfs_level))
        for m in individual.messages:
            if scenario.graphs[graph].arcs[m].task_from==task:
                task_to=scenario.graphs[graph].arcs[m].task_to
                if task_start[task_to]<(task_start[task]+(scenario.graphs[graph].tasks[task].wcet[mapped]*dvfs_level)):
                    task_start[task_to]=(task_start[task]+(scenario.graphs[graph].tasks[task].wcet[mapped]*dvfs_level))
    inc=0
    for cluster in individual.task_cluster:
        inc+=1
        mapped=individual.task_cluster[cluster].mapped_to
        print("Cluster",inc,"is Mapped to PE",mapped)
        for task in individual.task_cluster[cluster].tasks:
            print("Time",task,"starts executing is",task_start[task])

    max_time=0
    for cluster in cluster_time:
        if(cluster_time[cluster]>max_time):
            max_time=cluster_time[cluster]
    return (energy,max_time)

def matefunc(ind1,ind2):
    complete="complete"
    #print("crossover starts")
    for a in ind1.pbp_data[complete].decision_strat:
        if random.randint(0,1)==1:
            yo=ind1.pbp_data[complete].decision_strat[a]
            ind1.pbp_data[complete].decision_strat[a]=ind2.pbp_data[complete].decision_strat[a]
            ind2.pbp_data[complete].decision_strat[a]=yo
    #process constraints
    process_cons(ind1)
    process_cons(ind2)
    return ind1, ind2

def mutatefunc(ind,indpb=0.1):
    complete="complete"
    #print("Mutate starts")
    for a in ind.pbp_data[complete].decision_strat:
        if random.random() < indpb:
            ind.pbp_data[complete].decision_strat[a][1]= not ind.pbp_data[complete].decision_strat[a][1]
            yo=ind.pbp_data[complete].decision_strat[a][0]%1
            ind.pbp_data[complete].decision_strat[a][0]=(yo+ind.generation)
    ind.generation+=1
    process_cons(ind)
    #process constraints
    return ind

creator.create("Fitness", base.Fitness, weights=(1.0,1.0))
creator.create("Individual",Constraint_graph,fitness=creator.Fitness)

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
toolbox.register("select", tools.selTournament, tournsize=3)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_tgff", help="*.tgff file to parse")
    parser.add_argument("--tg", help="*name of task_graph",default="TASK_GRAPH")
    parser.add_argument("--modular","-m",default=0,help="Use modular or complete clustering, Modular=1/Complete=0")
    parser.add_argument("--core", help="name of core/PE", default="CLIENT_PE")
    parser.add_argument("-d", "--dir",default="./lp_files", help="output directory")
    parser.add_argument("-o", "--out",action="store", dest="out", default="ilp.lp", help="output file")
    parser.add_argument("--dvfs_level","--dvfs",action="store", dest="dvfs_num_levels", type=int, default=None, help="The number of dvfs_levels possible for each processor")
    args = parser.parse_args()
    global scenario
    scenario = Complete_Scenario()
    #saving the number of dvfs levels taken as input
    scenario.dvfs=args.dvfs_num_levels
    with open(args.input_tgff) as input_file:
        for block in get_blocks(input_file):
            process_block(block,args.tg,args.core)
    generate_noc(8,8)
    populate_task_params()
    if args.dvfs_num_levels!=None:
        scenario.dvfs=args.dvfs_num_levels
    else:
        scenario.dvfs=1
    gen_dvfslevel(args.dvfs_num_levels)
    phase=0

    #Processing each graph seperately
    for graph in scenario.graphs:
        #print_app_graph(graph)
        con_graph=Constraint_graph()
        con_graph.graph=graph
        gen_comp_pb(con_graph,graph)
        #print_pb_strat(con_graph)
        con_graph.pbp_data["complete"].assignment=process_pbp_data(con_graph)
        # isassigned,con_graph.pbp_data["complete"].assignment=dpll_solver(con_graph.pbp_data["complete"].decision_strat,con_graph.pbp_data["complete"].constraints,0)
        # if not isassigned:
        #     print("Clustering constraints broken, fix now")
        pop=None
        #print("Assignment by PB Solver Complete")
        gen_comp_con_graph(con_graph,graph)
        feasiblity_con_graph(con_graph,graph)
        evalParams(con_graph)
        continue
        print(f"Generating Population for {graph}")
        pop = toolbox.population(graph_name=graph,pop_size=5)
        # CXPB  is the probability with which two individuals
        #       are crossed
        #
        # MUTPB is the probability for mutating an individual
        CXPB, MUTPB = 0.5, 0.2

        print("Start of evolution", graph)

        # Evaluate the entire population
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
            print(fit)

        print("  Evaluated %i individuals" % len(pop))

        fits = [ind.fitness.values[0] for ind in pop]
        # Variable keeping track of the number of generations
        g = 0
        # Begin the evolution
        while g < 5:
            # A new generation
            g = g + 1
            print("-- Generation %i --" % g)

            # Select the next generation individuals
            offspring = toolbox.select(pop, len(pop))
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
                print(fit)
            #print("  Evaluated %i individuals" % len(invalid_ind))

            # The population is entirely replaced by the offspring
            pop[:] = offspring

            # Gather all the fitnesses in one list and print the stats
            fits = [ind.fitness.values[0] for ind in pop]
            fits += [ind.fitness.values[1] for ind in pop]
            print(fits)
            length = len(pop)
            mean = sum(fits) / length
            sum2 = sum(x*x for x in fits)
            std = abs(sum2 / length - mean**2)**0.5

            print("  Min %s" % min(fits))
            print("  Max %s" % max(fits))
            print("  Avg %s" % mean)
            print("  Std %s" % std)

        print("-- End of (successful) evolution --")

        best_ind = tools.selBest(pop, 1)[0]
        print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
        break
        phase+=1
    return
if __name__ == '__main__':
    main()
