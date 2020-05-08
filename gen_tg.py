import os
import sys
import re
import argparse
import random
import subprocess

def gen_opt(opt_path,num_task):
    print("Generating tgffopt file")
    seed_value=10
    num_graphs=4
    task_count=num_task
    task_type_cnt=40
    with open(opt_path, 'w') as f:
        f.write(f"seed {seed_value}\n")
        f.write("tg_label TASK_GRAPH\n")
        f.write(f"tg_cnt {num_graphs}\n")
        f.write(f"task_cnt {task_count} 0.5\n")
        f.write(f"task_type_cnt {task_type_cnt}\n")
        f.write(f"period_mul 1\n")
        f.write(f"task_trans_time 1\n")
        f.write(f"task_degree 2 3\n")
        #Important to keep each task unique in our DSE
        f.write(f"task_unique false\n")
        f.write(f"tg_write\n")
        f.write(f"eps_write\n")


def extend_tg(tg_path,template):
    print("adding template to end of generated file")
    with open(template, 'r') as f:
        contents=f.readlines()
    with open(tg_path, 'a') as f:
        f.writelines(contents)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--template","-t", help="The template file",default="./template.tgff")
    parser.add_argument("-d", "--dir",default="./tg_generated", help="output directory")
    parser.add_argument("-o", "--out",action="store", dest="out", default="trial", help="Name of the output file")
    parser.add_argument("-n","--num",default="20", help="The number of tasks in the graph")
    parser.add_argument("--tgff",default="./tgff-3.6/tgff",help="Path of the tgff binary")

    args = parser.parse_args()
    opt_path=os.path.join(args.dir,f"{args.out}.tgffopt")
    tg_path=os.path.join(args.dir,f"{args.out}.tgff")
    filename=os.path.join(args.dir,args.out)
    gen_opt(opt_path,args.num)
    opt_path=os.path.abspath(opt_path)
    output_run=subprocess.run([args.tgff,filename], capture_output=True)
    print(str(output_run.stdout))

    extend_tg(tg_path,args.template)


if __name__ == '__main__':
    main()
