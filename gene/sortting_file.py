
import os
import pandas as pd

foldname = "encode_lasso"

os.chdir(os.pardir) # cd ..
filename_list = os.listdir(foldname)
os.chdir(foldname)

for filename in filename_list:
    print filename
    csvfile = pd.read_csv(filename, header=None)
    csvfile = csvfile.sort_values([2], ascending=False)
    csvfile.to_csv(filename, header=False, index=False)