#the example from https://github.com/MIT-LCP/wfdb-python/blob/master/demo.ipynb.
#you need to install the package wfdb-python from pycharm.

import wfdb
import numpy as np
import os
from IPython.display import display

# Demo 1 - Read a wfdb record using the 'rdsamp' function into a wfdb.Record object.
# Plot the signals, and show the data.
record = wfdb.rdsamp('../sampledata/a103l')
wfdb.plotrec(record, title='Record a103l from Physionet Challenge 2015')
display(record.__dict__)

#read our own ecg data
record = wfdb.rdsamp('../ptbdb/patient001/s0010_re')
wfdb.plotrec(record, title='ecg data of patient 001')
display(record.__dict__)


# Demo 2 - Read certain channels and sections of the WFDB record using the simplified 'srdsamp' function
# which returns a numpy array and a dictionary. Show the data.
signals, fields=wfdb.srdsamp('../sampledata/s0010_re', channels=[14, 0, 5, 10], sampfrom=100, sampto=15000)
display(signals)
display(fields)

