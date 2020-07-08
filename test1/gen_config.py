import math
import types
import os
import sys
import re
import argparse
import yaml
import configparser
from collections import OrderedDict

config_num=0

def create_config(config,run_dict,num,output_path):
    global config_num
    if num>=len(run_dict):
        with open(f'{output_path}/config{config_num}.ini', 'w') as configfile:
            config.write(configfile)
        config_num+=1
        return
    else:
        temp_val=list(run_dict.keys())[num]
        for val in run_dict[temp_val]:
            if "objective_scale" in temp_val:
                config['GA_type'][str(temp_val)]=str(val)
            elif "dvfs" or "implementation" in temp_val:
                config['Cross_Layer_parameters'][str(temp_val)]=str(val)
            elif "num_tasks" in temp_val:
                config['Input_data'][str(temp_val)]=str(val)
                config['Input_data']['output_name']=f"tg_{val}"
                config['Input_data']['tgff']='synthetic'
            config['Output_data']['output_dir']=f"./results/test1/result{config_num}"
            config['Output_data']['cons_output']=f"./cons/test1/cons{config_num}"
            create_config(config,run_dict,(num+1),output_path)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--c",help="Complete path of *.ini config template",default="template.in")
    parser.add_argument("--y",help="Complete path of YAML run file",default="./run.yaml")
    parser.add_argument("--output_dir","-o",help="output path of the Configuration files",default=".")
    args = parser.parse_args()

    Config = configparser.ConfigParser()
    Config.read(args.c)

    run_data=None
    with open(args.y) as f:
        run_data= yaml.load_all(f, Loader=yaml.FullLoader)
        i=0
        run_dict=OrderedDict()
        for a in run_data:
            for param, vals in a.items():
                run_dict[param]=vals

    create_config(Config,run_dict,0,os.path.abspath(args.output_dir))






if __name__ == '__main__':
    main()
