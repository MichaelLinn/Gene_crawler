# coding=utf-8

import urllib2
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import pymongo
import os



class Gene_scraper:

    def dealCSV(self):

        os.chdir(os.pardir)
        foldname = "encoderoadmap_lasso"
        filename_list = os.listdir(foldname)
        os.chdir(foldname)
        sid = 0
        for filename in filename_list:
            sid = sid + 1
            print filename
            pair1fname = "pair1/" + "sample" + str(sid) + "pair1.fasta"
            pair2fname = "pair2/" + "sample" + str(sid) + "pair2.fasta"
            p1File = open(pair1fname, "a")
            p2File = open(pair2fname, "a")
            file = open(filename, "r")

            for i in range(1, 200, 2):
                gene_list = file.readline().split(",")
                promoterSeq = self.dealFirstGeneStr(gene_list[0])  # promoterSeq
                p1File.write((">seq"+str(i)+"\n"))
                p1File.write(promoterSeq + "\n")
                p1File.write((">seq" + str(i+1) + "\n"))
                p1File.write(promoterSeq + "\n")
                upSeq, downSeq = self.dealSecondGeneStr(gene_list[1])  # geneUpStream & geneDownStream
                p2File.write((">seq" + str(i) + "\n"))
                p2File.write(upSeq + "\n")
                p2File.write((">seq" + str(i+1) + "\n"))
                p2File.write(downSeq + "\n")

            p1File.close()
            p2File.close()
            file.close()

    def dealFirstGeneStr(self, gString):

        _, gType, gStart, gEnd = re.split("chr|:|-", gString.strip())
        print gType, gStart, gEnd
        return self.getSeqFromWeb(gType, gStart, gEnd)


    def dealSecondGeneStr(self, gString):
        list = gString.split(".")
        geneName = list[0]
        print geneName
        up, down = self.getUDGeneSeq(geneName)
        return up, down

    def getSeqFromWeb(self, gType, gStart, gEnd):

        url = "http://genome.ucsc.edu/cgi-bin/das/hg19/dna?segment=chr"

        gene_url = url + gType + ":" + str(gStart) + "," + str(gEnd)
        print gene_url

        req = urllib2.Request(gene_url)
        resp = urllib2.urlopen(req)
        geneHtml = resp.read()

        geneSoup = BeautifulSoup(geneHtml, "xml")

        geneSeq =  geneSoup.find("DNA").contents[0].strip().replace("\n","")

        print geneSeq

        return geneSeq

    def getUDGeneSeq(self, gene_name):

        gene_name = "ENSG00000138385"
        url = "http://grch37.ensembl.org/Homo_sapiens/Gene/Summary?db=core;g=" + gene_name
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
        print "************upstream gene sequence************"
        upSeq = self.getSeqFromWeb(type, gStart - 1000, gStart - 1)
        print "************downstream gene sequence************"
        downSeq = self.getSeqFromWeb(type, gEnd + 1, gEnd + 1000)
        return upSeq, downSeq

    def buildFasta(self, geneSeq, idx, filename):


        return 0


if __name__ == "main":

    print os.getcwd()
    tem = Gene_scraper()
    tem.dealCSV()

print os.getcwd()
tem = Gene_scraper()
tem.dealCSV()
# tem.getGeneSeq()