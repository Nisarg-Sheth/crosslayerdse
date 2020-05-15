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
#from deap.benchmarks.tools import hypervolume
from pygmo import hypervolume
import configparser

scenario = None
random.seed(124)

def main():
    print("yo")
    Config = configparser.ConfigParser()
    Config.read('config.ini')
    print(Config.sections())
    print(Config.get('Meta_data','individuals'))

    return

if __name__ == '__main__':
    main()
