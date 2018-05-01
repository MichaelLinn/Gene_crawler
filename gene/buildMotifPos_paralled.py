# -*- coding: utf-8 -*-
# @Time    : 4/25/18 3:03 PM
# @Author  : Jason Lin
# @File    : buildMotifPos_paralled.py
# @Software: PyCharm

import pandas as pd
import os
import urllib2
from bs4 import BeautifulSoup
import re
import subprocess
import concurrent.futures
import glob
import random
import time



def grab_motif_info(filename):
    encode_no = filename.split(".")[1]
    file = open(filename, "r")
    motif_info = []
    for j in range(1, 200, 2):
        gene_list = file.readline().split(",")
        print gene_list

        # add waiting time to cheat the anti-crawler
        # time.sleep(random.random()*3)

        promoterInfo = gene_list[0]  # promoterSeq
        geneName = gene_list[1].split(".")[0]

        upEnhancer, downEnhancer = getPositionOfEnhancer(geneName)  # geneUpStream & geneDownStream

        chr_type = "chr" + str(upEnhancer[0])
        upE = chr_type + ":" + str(upEnhancer[1]) + "-" + str(upEnhancer[2])
        downE = chr_type + ":" + str(downEnhancer[1]) + "-" + str(downEnhancer[2])

        # title = ["chr_type", "promoter", "gene", "up_enhancer", "down_enhancer", "encode_no"]
        tem = [chr_type, promoterInfo, geneName, upE, downE, encode_no]
        motif_info.append(tem)
    return motif_info


def getPositionOfEnhancer(gene_name):

    url = "http://grch37.ensembl.org/Homo_sapiens/Gene/Summary?db=core;g=" + gene_name
    print url
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)

    respHtml = resp.read()
    soup = BeautifulSoup(respHtml, "lxml")

    list = soup.body.find("a", class_="constant")
    href = list.attrs['href'].split(";")
    type, gStart, gEnd = re.split(":|-", href[2])
    type = type.split("=")[1]
    gStart = int(gStart)
    gEnd = int(gEnd)
    upSeq = [type, gStart - 1000, gStart - 1]
    downSeq = [type, gEnd + 1, gEnd + 1000]
    return upSeq, downSeq

motif_info_list = []
with concurrent.futures.ProcessPoolExecutor() as executor:
    os.chdir(os.pardir)
    print os.getcwd()
    foldname = "encode_lasso"
    os.chdir(foldname)
    filename_list = glob.glob(r"*.csv")
    print filename_list
    # motif_ = open("motif_position.csv", "r")
    title = ["chr_type", "promoter", "gene", "enhancer_up", "enhancer_down", "encode_no"]

    # input : filename_list
    for pair, result in zip(filename_list, executor.map(grab_motif_info, filename_list)):
        print(pair, result)
        motif_info_list += result

motif_df = pd.DataFrame(motif_info_list)
motif_df.columns = title
motif_df.to_csv("../motif_encode.csv", index=False)

