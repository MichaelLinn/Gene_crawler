# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

data = pd.read_excel("nature.xlsx")

for index, row in data.iterrows():
    for i in range(len(row)):
        # print row[i]
        tem = str(row[i])
        if tem == "nan":
            s = str(row.index[i]) + "-" + str(index)
            print s





