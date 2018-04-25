# -*- coding: utf-8 -*-
# @Time    : 3/23/18 2:36 PM
# @Author  : Jason Lin
# @File    : paralleled_motifhyades.py
# @Software: PyCharm Community Edition

import concurrent.futures
import os
import glob
import multiprocessing
import subprocess

os.chdir(os.pardir)
print os.getcwd()


f_l1 = glob.glob(r"encode_lasso/pair1/*.fasta")
f_l2 = glob.glob(r"encode_lasso/pair1/*.fasta")

def run_MotifHyades(pair):
    p1, p2, w_1, w_2 = pair
    f_v81 = "/usr/local/MATLAB/MATLAB_Compiler_Runtime/v81"
    n_motifpair = '20'
    subprocess.call(["motif_test/run_MotifHyades.sh", f_v81, p1, p2, w_1, w_2, n_motifpair])

    return "success!"



with concurrent.futures.ProcessPoolExecutor() as executor:
    f_l1 = glob.glob(r"encode_lasso/pair1/*.fasta")
    f_l2 = glob.glob(r"encode_lasso/pair2/*.fasta")
    pair_list = []
    motif_width = ['10', '15', '25']
    n_motifpair = '20'

    for p1 in f_l1:
        for p2 in f_l2:
            if p1.split("_")[3] == p2.split("_")[3]:
                for w_1 in motif_width:
                    for w_2 in motif_width:
                        pair_list.append([p1, p2, w_1, w_2])
                        print [p1, p2, w_1, w_2]

    # Process the list of files, but split the work across the process pool to ues all CPUs!
    for pair, result in zip(pair_list, executor.map(run_MotifHyades, pair_list)):
        print(pair, result)

