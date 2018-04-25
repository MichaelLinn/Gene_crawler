# coding=utf-8

import urllib2
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import os



class Gene_scraper:

    def dealCSV(self):

        os.chdir(os.pardir)
        foldname = "encode_lasso"
        filename_list = os.listdir(foldname)
        print filename_list
        os.chdir(foldname)
        for i in range(len(filename_list)):
            filename = filename_list[i]
            print "filename: ", filename
            if filename == "pair1" or filename == "pair2":
                continue
            no_ = filename.split(".")[1]
            pair1fname = "pair1/" + str(i) + "_encode_" + no_ + "_1.fasta"
            pair2fname = "pair2/" + str(i) + "_encode_" + no_ + "_2.fasta"
            p1File = open(pair1fname, "a")
            p2File = open(pair2fname, "a")
            file = open(filename, "r")

            for j in range(1, 200, 2):
                gene_list = file.readline().split(",")
                promoterSeq = self.dealFirstGeneStr(gene_list[0])  # promoterSeq
                p1File.write((">seq"+str(j)+"\n"))
                p1File.write(promoterSeq + "\n")
                p1File.write((">seq" + str(j+1) + "\n"))
                p1File.write(promoterSeq + "\n")

                upSeq, downSeq = self.dealSecondGeneStr(gene_list[1])  # geneUpStream & geneDownStream
                p2File.write((">seq" + str(j) + "\n"))
                p2File.write(upSeq + "\n")
                p2File.write((">seq" + str(j+1) + "\n"))
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
        print "************upstream gene sequence************"
        upSeq = self.getSeqFromWeb(type, gStart - 1000, gStart - 1)
        print "************downstream gene sequence************"
        downSeq = self.getSeqFromWeb(type, gEnd + 1, gEnd + 1000)
        return upSeq, downSeq


    # build a csv to record the position of potential enhencer and promoter
    def buildMotifPositionFile(self):
        os.chdir(os.pardir)
        foldname = "encode_lasso"
        filename_list = os.listdir(foldname)
        print filename_list
        os.chdir(foldname)

        # motif_ = open("motif_position.csv", "r")
        title = ["chr_type", "promoter", "gene", "enhancer", "encode_no"]
        motif_info_list = []

        for i in range(len(filename_list)):
            filename = filename_list[i]
            print "filename: ", filename
            if filename == "pair1" or filename == "pair2":
                continue
            encode_no = filename.split(".")[1]

            file = open(filename, "r")

            for j in range(1, 200, 2):
                gene_list = file.readline().split(",")
                print gene_list

                promoterInfo = gene_list[0]  # promoterSeq
                geneName = gene_list[1].split(".")[0]

                upEnhancer, downEnhancer = self.getPositionOfEnhancer(geneName)  # geneUpStream & geneDownStream

                chr_type = "chr" + str(upEnhancer[0])
                upE = chr_type + ":" + str(upEnhancer[1]) + "-" + str(upEnhancer[2])
                downE = chr_type + ":" +  str(downEnhancer[1]) + "-" + str(downEnhancer[2])

                # title = ["chr_type", "promoter", "gene", "enhancer", "encode_no"]
                temU = [chr_type, promoterInfo, geneName, upE, encode_no]
                temD = [chr_type, promoterInfo, geneName, downE, encode_no]

                motif_info_list.append(temU)
                motif_info_list.append(temD)

            file.close()
            break

        motif_df = pd.DataFrame(motif_info_list)
        motif_df.columns = title
        motif_df.to_csv("../motif_encode.csv", index=False)

    def getPositionOfEnhancer(self, gene_name):

        # gene_name = "ENSG00000138385"
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


if __name__ == "__main__":

    print os.getcwd()
    tem = Gene_scraper()
    tem.buildMotifPositionFile()






