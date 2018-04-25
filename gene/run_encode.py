# -*- coding: utf-8 -*-
# @Time    : 2/2/18 4:22 PM
# @Author  : Jason Lin
# @File    : run_encode.py
# @Software: PyCharm Community Edition
import os
import subprocess

os.chdir(os.pardir)
print os.getcwd()

f_p1 = "encode_lasso/pair1/"
f_p2 = "encode_lasso/pair2/"

f_l1 = os.listdir(f_p1)
f_l2 = os.listdir(f_p2)

f_v81 = "/usr/local/MATLAB/MATLAB_Compiler_Runtime/v81"

motif_width = ['10', '15', '20']
n_motifpair = '20'



for p1 in f_l1:
    for p2 in f_l2:
        if p1.split("_")[0] == p2.split("_")[0]:
            print p1, p2
            for w_1 in motif_width:
                for w_2 in motif_width:
                    subprocess.call(["motif_test/run_MotifHyades.sh", f_v81, f_p1+p1, f_p2+p2, w_1, w_2, n_motifpair])
