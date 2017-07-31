# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 14:32:36 2016

@author: gai72996
"""

import numpy as np
import argparse


def get_lines(path):
    with open(path) as f:
        lines = f.read().splitlines()
    f.close()
    return lines


def write_lines(path, lines):
    f = open(path, 'w')
    for l in lines:
        f.write(l)
        f.write("\n")
    f.close()


def write_jsf_sub(ofpath):
    """ """
    sub_lines = []
    sub_lines.append("# mcnpx simulation")
    sub_lines.append("#BSUB -q scarf")
    sub_lines.append("#BSUB -n 1")
    sub_lines.append("#BSUB -o %J.log")
    sub_lines.append("#BSUB -e %J.err")
    sub_lines.append("")
    sub_lines.append("mcnpx_isis_270X n=" + ofpath)

    ofpath = ofpath + ".sh"
    write_lines(ofpath, sub_lines)


def write_launch_script(ospath, of_names):
    """ """
    script_lines = []
    script_lines.append("#!/bin/bash")
    script_lines.append("module load contrib/neutronics/ISIS_MCNPX")
    script_lines.append("")

    for n in of_names:
        script_lines.append("echo submitting job") # required to slow sub down
        script_lines.append("bsub < "+n+".sh")

    write_lines(ospath, script_lines)


def first_index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
            return i
    return -1


def make_run(in_path, nfiles, ospath="launch.sh"):
    """ """

    of_names = []
    mcnp_lines = get_lines(in_path)
    # find DBCN position in inputfile, check both lower and upper case
    DBCN_ln = first_index_containing_substring(mcnp_lines, "dbcn")
    if DBCN_ln == -1:
        DBCN_ln = first_index_containing_substring(mcnp_lines, "DBCN")
    # check if there are any DBCN variables after the seed
    if len(mcnp_lines[DBCN_ln].split(" ")) > 2:
        DBCN_end = mcnp_lines[DBCN_ln].split(" ")[1:]
    else:
        DBCN_end = " "

    i = 0
    while i < nfiles:
        of_name = in_path + str(i)
        of_names.append(of_name)
        # new get new random seed, seed must be odd
        rn = np.random.randint(1e8, 1e10)
        if rn % 2 == 0:
            rn = rn + 1
        mcnp_lines[DBCN_ln] = "DBCN " + str(rn) + DBCN_end
        write_lines(of_name, mcnp_lines)
        write_jsf_sub(of_name)
        i = i + 1

    write_launch_script(ospath, of_names)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="setup and run multiple" +
                   " copies of the same mcnpx run with different seeds")
    parser.add_argument("input_file", help="path to mcnpx input file")
    parser.add_argument("n_jobs",  help="number of jobs to create", type=int)
    parser.add_argument("-o", "--output", action="store", dest="output",
                        help="output file name for script that runs jobs")
    args = parser.parse_args()
    if args.output:
        make_run(args.input_file, args.n_jobs, args.output)
    else:
        make_run(args.input_file, args.n_jobs)
