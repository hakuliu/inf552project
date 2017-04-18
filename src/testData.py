#the example from https://github.com/MIT-LCP/wfdb-python/blob/master/demo.ipynb.
#you need to install the package wfdb-python from pycharm.

import wfdb
import numpy as np
import os
from IPython.display import display




#read our own ecg data
record = wfdb.rdsamp('../ptbdb/patient002/s0015lre')
wfdb.plotrec(record, title='ecg data of patient 001')
display(record.__dict__)

print('test complete')