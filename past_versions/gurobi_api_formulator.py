
import math
import types
import os
import sys
import re
import argparse
import gurobipy as gp
from gurobipy import GRB

scenario = None


class Complete_Scenario:
    def __init__(self):
        self.attributes = {}
        self.graphs = {}
        self.tables = {}
        self.hyperperiod = None

class Graph:
    def __init__(self,name,period):
        self.name = name
        self.period = period
        self.num_of_tasks = 0
        self.num_of_arcs = 0
        self.tasks = {}
        self.task_name =[]
        self.arcs = {}
        self.arc_name=[]
        self.deadline = {}

    def add_task(self,task_details):
        task_dets=task_details.split()
        self.num_of_tasks+=1
        self.task_name.append(task_dets[0])
        self.tasks[task_dets[0]]=Task(task_dets[0],int(task_dets[2]),int(task_dets[4]))
        #create a new task with      :name       ,type          ,host
    def add_arc(self,arc_details):
        arc_dets=arc_details.split()
        self.num_of_arcs+=1
        self.arc_name.append(arc_dets[0])
        self.arcs[arc_dets[0]]=Arc(arc_dets[0],arc_dets[2],arc_dets[4],arc_dets[6])
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
        self.predecessor = []
        self.successor = []
        self.hard_deadline = None
        self.soft_deadline = None
class Arc:
    def __init__(self,name,pe_from,pe_to,type):
        self.name=name
        self.pe_from=pe_from
        self.pe_to=pe_to
        self.type=type

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
        scenario.tables[core_name]=Table(core_name,block[1].strip('#'),block[2].strip('#'),block[4].strip('#'))
        for i in range(5, len(block)):
            if not block[i].startswith('#'):
                scenario.tables[core_name].add_row(block[i])
    elif "HYPERPERIOD" in block[0]:
        scenario.hyperperiod= float(block[0].strip('@HYPERPERIOD '))

def populate_wcet():
    global scenario
    for graph in scenario.graphs:
        for task in scenario.graphs[graph].tasks:
            type_of_task=scenario.graphs[graph].tasks[task].type
            for table in scenario.tables:
                if scenario.tables[table].values[type_of_task][0]==type_of_task:
                    if int(scenario.tables[table].values[type_of_task][2])==1:
                        scenario.graphs[graph].tasks[task].pe_list.append(table)
                        scenario.graphs[graph].tasks[task].wcet[table]=float(scenario.tables[table].values[type_of_task][3])

def generate_ILP(output_file, graph):
    global scenario
    c_list=[]
    service_level=10
    hop_level=(4*4)-2
    map_list=[]
    map_vars=[]
    for task in graph.tasks:
        map_list.append(graph.tasks[task].pe_list)
    for task1 in graph.tasks:
        for task2 in graph.tasks:
            c_list.append(task1+"_"+task2)
    num_of_con=0;
    con_val= "constraint"
    pluss=" + "
    minuss=" - "
    equalss=" = "
    lessthan=" <= "

    #GUROBI model
    gb_model = gp.Model("binary_ilp")

    #Declare the variables as binary
    master_vars=gb_model.addVars(graph.task_name, name="master")
    slave_vars=gb_model.addVars(graph.task_name, name="slave")
    for task in graph.tasks:
        map_vars.append(gb_model.addVars(graph.tasks[task].pe_list, name=task))
    c_vars=gb_model.addVars(c_list, name="C")


    #set objective function, trivial in our case
    gb_model.setObjective(locals()[slave_list[0]], GRB.MINIMIZE)

    #Adding the Constraints



    with open(output_file, 'w') as f:
        f.write("Minimize\n")
        f.write("problem: "+slave_list[0]+"\n")
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
            line=pluss+str(graph.num_of_tasks-(i+1))+" "+master_list[i]
            for j in range((i+1),graph.num_of_tasks):
                line=line+pluss+" 1 "+c_list[(i*graph.num_of_tasks)+j]
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
                line = line + pluss + " 1 " +"map_t"+str(i)+j
            line = line + equalss + "0"
            f.write(con+line+"\n")

            #verifying that mapping is not bad.
            for j in range(i):
                num_of_con+=1
                con = con_val+"_"+str(num_of_con)+ " : "
                line=minuss+" 1 "+c_list[(i*graph.num_of_tasks)+j]
                for pe in map_list[i]:
                    if pe in map_list[j]:
                        line = line + pluss + " 1 " +"map_t"+str(j)+pe
                line = line + equalss + "0"
                f.write(con+line+"\n")
            for j in range((i+1),graph.num_of_tasks):
                num_of_con+=1
                con = con_val+"_"+str(num_of_con)+ " : "
                line=minuss+" 1 "+c_list[(i*graph.num_of_tasks)+j]
                for pe in map_list[i]:
                    if pe in map_list[j]:
                        line = line + pluss + " 1 " +"map_t"+str(j)+pe
                line = line + equalss + "0"
                f.write(con+line+"\n")

        for m in graph.arcs:

            #service level for each message
            num_of_con+=1
            con = con_val+"_"+str(num_of_con)+ " : "
            line=""
            for j in range(service_level):
                line= line +pluss+" 1 "+"sl_"+str(j)+m
            line = line + equalss + "1"
            f.write(con+line+"\n")

            #maximum hop distance for each message
            num_of_con+=1
            con = con_val+"_"+str(num_of_con)+ " : "
            line=""
            for j in range(hop_level):
                line= line +pluss+" 1 "+"hop_"+str(j+1)+m
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
                f.write("map_t"+str(i)+j+"\n")
                num_var+=1

        for m in graph.arcs:
            for j in range(service_level):
                f.write("sl_"+str(j)+m+"\n")
                num_var+=1
            for j in range(hop_level):
                f.write("hop_"+str(j+1)+m+"\n")
                num_var+=1
        print("The number of variables: "+str(num_var))
        f.write("End\n")
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_tgff", help="*.tgff file to parse")
    parser.add_argument("--tg", help="*name of task_graph",default="TASK_GRAPH")
    parser.add_argument("--core", help="name of core/PE", default="CLIENT_PE")
    parser.add_argument("-d", "--dir",default=".", help="output directory")
    parser.add_argument("-o", "--out",action="store", dest="out", default="ilp.lp", help="output file")
    args = parser.parse_args()

    global scenario
    scenario = Complete_Scenario()
    with open(args.input_tgff) as input_file:
        for block in get_blocks(input_file):
            process_block(block,args.tg,args.core)
    populate_wcet()

    phase=0
    #the ILP formulation

    for graph in scenario.graphs:
        out_name=args.out
        ext_id = out_name.rfind(".")
        prefix = out_name[:ext_id]
        ext = out_name[ext_id+1:]
        out_name = "%s.%d.%s" % (prefix, phase, ext)
        generate_ILP(os.path.join(args.dir,out_name),scenario.graphs[graph])
        phase+=1

if __name__ == '__main__':
    main()
