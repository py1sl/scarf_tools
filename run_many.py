"""
"""
import numpy as np
import subprocess
import os

MCNP_file = "Chip_sl"
nruns = 20

def first_index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
              return i
    return -1

    
def write_lines(path, lines):
    f = open(path, 'w')
    for l in lines:
        f.write(l)
        f.write("\n")
    f.close()

    
def get_lines(path):
    with open(path) as f:
        lines = f.read().splitlines()
    f.close()
    return lines
    
def write_job_script(fname, sname):
    sub_lines = []
    sub_lines.append("# MCNP run")
    sub_lines.append("#BSUB -q scarf")
    sub_lines.append("#BSUB -n 1")
    sub_lines.append("#BSUB -o %J.log")
    sub_lines.append("#BSUB -e %J.err")
    sub_lines.append("#BSUB -W 48:00")
    sub_lines.append(" ")
    sub_lines.append("mpirun -lsf /home/isisg/scarf473/my_mcnp/MCNP_CODE/MCNP6/bin/mcnp6.mpi n=" + fname + " XSDIR=/home/isisg/scarf473/my_mcnp/mcnpx_data/xsdir wwinp=wwinp2")
    
    write_lines(sname, sub_lines)
    
    
lines = get_lines(MCNP_file)
rand_line = first_index_containing_substring(lines, "RAND")

indexes = np.arange(nruns)
rands = np.random.randint(100000, 1000000000, size=(nruns))
rscript = []
rscript.append("#!/bin/bash")


for i in indexes:
    oname = MCNP_file + "_" + str(i) + "."
    sname = "que_" + str(i) + ".sh" 
    lines[rand_line] = "RAND gen=2 seed=" + str(rands[i])
    write_lines(oname, lines)
    write_job_script(oname, sname)
    rscript.append("bsub < " + sname)
    

write_lines("run.sh", rscript)
os.chmod("run.sh", 0700)
subprocess.call(["./run.sh"])
    
    


