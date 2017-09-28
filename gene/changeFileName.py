
import os
os.getcwd()
os.chdir(os.pardir)
os.chdir("encoderoadmap_lasso")
os.chdir("pair2")
print os.getcwd()
for i in range(2,128):
    print i
    f1 = "sample" + str(i) + "pair1.fasta"
    f2 = "sample" + str(i) + "pair2.fasta"
    print f1
    os.rename(f1, f2)

