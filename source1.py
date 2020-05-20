import os
import sys
import re
import argparse
import subprocess
from graphviz import Digraph
from collections import OrderedDict

class Complete_Scenario:
    def __init__(self):
        self.attributes = {}
        self.graphs = {}
        self.all_tables= OrderedDict()
        self.NOC=[]
        self.tables = {}
        self.hyperperiod = None
        self.constraint_graphs = {}
        self.dvfs=None
        self.dvfs_level = []
        self.service_level = 10
        self.max_hop=14
        self.communication={}
        self.single_pop_size=20
        self.pop_size=100
        self.isConstrained=False
        self.objective_scale_energy=4
        self.objective_scale_time=4
        self.baseline_value_time=2000
        self.baseline_value_energy=2000
class PB_data:
    def __init__(self):
        self.constraints = []
        self.decision_strat = OrderedDict()
        self.assignment = None
        self.max_priority=1

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

class Task_data:
    def __init__(self,name):
        self.name=name
        self.mapped= None
        self.dvfs_level = 1

class Gene_data:
    def __init__(self):
        self.pe=None
        self.dvfs=1

class Individual_data:
    def __init__(self):
        self.task_cluster = {}
        self.task_to_cluster = {}
        self.pbp_data=None
        self.pe_list={}
        self.task_list={}
        self.assignment= None
        self.generation = 1
        self.graph = None
        self.constraints =[]
        self.isFeasible =True

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
        self.constraints =[]
        self.lowest_time=None
        self.lowest_energy=None
        self.num_of_added_con=0
        self.num_of_vars = 0

    def add_task(self,task_details):
        task_details=task_details.replace("_","")
        #print(task_details)
        task_dets=task_details.split()
        self.num_of_tasks+=1
        self.tasks[task_dets[0]]=Task(task_dets[0],int(task_dets[2]))
        #create a new task with      :name       ,type          ,host
    def add_arc(self,arc_details,tg_name):
        arc_details=arc_details.replace("_","")
        arc_dets=arc_details.split()
        self.num_of_arcs+=1
        #IMP - ARCS are not unique in the benchmarks.
        #Need to make them unique

        arc_name=arc_dets[0]+str(self.num_of_arcs)
        self.arcs[arc_name]=Arc(arc_name,tg_name+arc_dets[2],tg_name+arc_dets[4],arc_dets[6])
        #create a new arc with    :name       ,pe_from    ,pe_to      ,type
        self.tasks[tg_name+arc_dets[2]].successor.append(tg_name+arc_dets[4])
        self.tasks[tg_name+arc_dets[4]].predecessor.append(tg_name+arc_dets[2])

    def add_hard_deadline(self,deadline_details,tg_name):
        deadline_details=deadline_details.replace("_","")
        deadline_dets=deadline_details.split()
        self.tasks[tg_name+deadline_dets[2]].hard_deadline=float(deadline_dets[4])

    def add_soft_deadline(self,deadline_details,tg_name):
        deadline_details=deadline_details.replace("_","")
        deadline_dets=deadline_details.split()
        self.tasks[tg_name+deadline_dets[2]].soft_deadline=float(deadline_dets[4])

class Task:
    def __init__(self,name,type,host=0):
        self.name = name
        self.type = type
        self.host = host
        self.pe_list = []
        self.num_of_pe = 0
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
