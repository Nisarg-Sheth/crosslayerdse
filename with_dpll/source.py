import os
import sys
import re
import argparse
import subprocess
from graphviz import Digraph
from collections import OrderedDict

class Complete_Scenario:
    def __init__(self):
        self.num_of_added_con=0
        self.attributes = {}
        self.graphs = {}
        self.all_tables={}
        self.NOC=[]
        self.tables = {}
        self.hyperperiod = None
        self.constraint_graphs = {}
        self.dvfs=None
        self.dvfs_level = []
        self.service_level = 10
        self.max_hop=14
        self.communication={}
class PB_data:
    def __init__(self):
        self.constraints = []
        self.decision_strat = OrderedDict()
        self.assignment = None

class Constraint_graph:
    def __init__(self):
        self.task_cluster = {}
        self.num_of_clusters = 0
        self.messages = {}
        self.task_to_cluster = {}
        self.dvfs_level = {}
        self.pbp_data = {}
        self.generation = 1
        self.graph = None
class Task_cluster:
    def __init__(self):
        self.mapped_to = None
        self.can_be_mapped = []
        self.tasks = []
class Message:
    def __init__(self):
        self.cluster_from = None
        self.cluster_to = None
        self.hop = None
        self.sl = None

class Graph:
    def __init__(self,name,period):
        self.name = name
        self.period = period
        self.num_of_tasks = 0
        self.num_of_arcs = 0
        self.tasks = {}
        self.arcs = {}
        self.deadline = {}
        self.num_of_evals=0

    def add_task(self,task_details):
        task_dets=task_details.split()
        self.num_of_tasks+=1
        self.tasks[task_dets[0]]=Task(task_dets[0],int(task_dets[2]))
        #create a new task with      :name       ,type          ,host
    def add_arc(self,arc_details):
        arc_dets=arc_details.split()
        self.num_of_arcs+=1
        #IMP - ARCS are not unique in the benchmarks.
        #Need to make them unique

        arc_name=arc_dets[0]+str(self.num_of_arcs)
        self.arcs[arc_name]=Arc(arc_name,arc_dets[2],arc_dets[4],arc_dets[6])
        #create a new arc with    :name       ,pe_from    ,pe_to      ,type
        self.tasks[arc_dets[2]].successor.append(arc_dets[4])
        self.tasks[arc_dets[4]].predecessor.append(arc_dets[2])

    def add_hard_deadline(self,deadline_details):
        deadline_dets=deadline_details.split()
        self.tasks[deadline_dets[2]].hard_deadline=float(deadline_dets[4])

    def add_soft_deadline(self,deadline_details):
        deadline_dets=deadline_details.split()
        self.tasks[deadline_dets[2]].soft_deadline=float(deadline_dets[4])

class Task:
    def __init__(self,name,type,host=0):
        self.name = name
        self.type = type
        self.host = host
        self.pe_list = []
        self.wcet = {}
        self.power = {}
        self.successor=[]
        self.predecessor=[]
        self.code_bits = {}
        self.preempt_time = {}
        self.priority=0
        self.hard_deadline = None
        self.soft_deadline = None
class Arc:
    def __init__(self,name,task_from,task_to,type):
        self.name=name
        self.task_from=task_from
        self.task_to=task_to
        self.type=type
        self.quant=5000.0

class Table:
    def __init__(self,name,attribute_row,raw_attribute_row,row4):
        self.name=name
        self.attributes= {}
        attr=attribute_row.split()
        attrval=raw_attribute_row.split()
        for i in range(len(attr)):
            self.attributes[attr[i]]=attrval[i]
        self.values  = []
        self.rows = row4.split()

    def add_row(self,row):
        row_values=[]
        for i in row.split():
            row_values.append(float(i))
        self.values.append(row_values)

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
        print(core_name)
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
    #SOME TRIAL PLOTTING
    constraint_g = Digraph(comment = graph)
    for task in scenario.constraint_graphs[graph].task_cluster:
        to_show="{"
        mapped_to = scenario.constraint_graphs[graph].task_cluster[task].mapped_to
        for a in scenario.constraint_graphs[graph].task_cluster[task].tasks:
            to_show=to_show+" "+a+","
        to_show=to_show+"}"
        to_show=to_show + "\n"+mapped_to
        constraint_g.node(task,label=to_show)
    for m in scenario.constraint_graphs[graph].messages:
        to_show="m"
        to_show=to_show + "\n"+str(scenario.constraint_graphs[graph].messages[m].sl)
        to_show=to_show + "\n"+str(scenario.constraint_graphs[graph].messages[m].hop)
        constraint_g.node(m,label=to_show)
        constraint_g.edge(scenario.constraint_graphs[graph].messages[m].cluster_from, m , constraint='false')
        constraint_g.edge(m,scenario.constraint_graphs[graph].messages[m].cluster_to , constraint='false')
    #constraint_g.render("./yo.view",view=True)

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
