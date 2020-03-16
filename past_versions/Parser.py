import math
import types
import os
import sys
import re
import argparse

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
        self.arcs = {}
        self.deadline = {}

    def add_task(self,task_details):
        task_dets=task_details.split()
        self.num_of_tasks+=1
        self.tasks[task_dets[0]]=Task(task_dets[0],int(task_dets[2]),int(task_dets[4]))
        #create a new task with      :name       ,type          ,host
    def add_arc(self,arc_details):
        arc_dets=arc_details.split()
        self.num_of_arcs+=1
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
        core_name= block[0].strip('@').strip('{')
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
                        #print(task)
                        #print(table)
                        #print(float(scenario.tables[table].values[type_of_task][3]))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_tgff", help="*.tgff file to parse")
    parser.add_argument("--tg", help="*name of task_graph",default="TASK_GRAPH")
    parser.add_argument("--core", help="name of core/PE", default="CLIENT_PE")
    args = parser.parse_args()

    global scenario
    scenario = Complete_Scenario()
    with open(args.input_tgff) as input_file:
        for block in get_blocks(input_file):
            process_block(block,args.tg,args.core)

    populate_wcet()


if __name__ == '__main__':
    main()
