# -*- coding: utf-8 -*-
# @Time    : 10/3/17 11:06 AM
# @Author  : Jason Lin
# @File    : gen_seqDict.py
# @Software: PyCharm Community Edition

import os

os.chdir(os.pardir)
foldname = "fantom5_lasso"
filename_list = os.listdir(foldname)

no_ = []
for filename in filename_list:
    if filename == ".." or filename == "." or filename == "pair1" or filename == "pair2":
        continue
    tem = filename.split(".")
    no_.append(tem[1])

print no_

os.chdir(foldname)
pairs = os.listdir("pair1")
os.chdir("pair1")

for i in range(len(pairs)):
    # print "--------"+ str(i) + "--------"
    new_name = "fantom5_" + no_[i] + "_1.fasta"
    print pairs[i] + "   " + new_name
    os.rename(pairs[i], new_name)

os.chdir(os.pardir)
pairs = os.listdir("pair2")
os.chdir("pair2")

for i in range(len(pairs)):
    # print "--------"+ str(i) + "--------"
    new_name = "fantom5_" + no_[i] + "_2.fasta"
    print pairs[i] + "   " + new_name
    os.rename(pairs[i], new_name)