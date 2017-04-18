"""
"""

import numpy as np
import subprocess
import os


def current_job_nums():
    lines = subprocess.check_output("bjobs")
    lines=lines.splitlines()
    lines=lines[1:]
    job_nums = []
    for l in lines:
        l=l.split(" ")
        if l[0] != "":
            job_nums.append(l[0])
    return job_nums
           
def get_lines(path):
    with open(path) as f:
        lines = f.read().splitlines()
    f.close()
    return lines
    
def check_status(jobs):
    all_status = []
    for job in  jobs:
        status = []
        status.append(job)
        lines = subprocess.check_output(["bpeek", job])
        lines=lines.splitlines()
        lines = lines[-3]
        print lines
        all_status.append(status)
        
def compare_running(fpath):
    """
    assume fpath points to a file with a list of job numbers each on a seperate line
    """
     
    all_status = []
    job_list = get_lines(fpath)
    running_jobs = current_job_nums()
     
    for job in job_list:
        status = []
        status.append(job)
        if job in running_jobs:
            status.append("Running")
        else:
            status.append("Finished")
        all_status.append(status)
    return all_status  
        


running_jobs = current_job_nums()
check_status(running_jobs)
statlist = compare_running("jlist")
print statlist




