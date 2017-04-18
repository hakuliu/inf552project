
import wfdb
import recordTranslator as rutil
import numpy as np
import os
from IPython.display import display
import matplotlib.pyplot as plt

#figure out what the average number of datapoints we're dealing with
# f = open('../ptbdb/RECORDS', 'r')
# for line in f:
#     rfile = '../ptbdb/' + line.strip();
#     record = wfdb.rdheader(rfile)
#     print(record.siglen)

#figure out what all possible diagnosis contained within this database
possible = []
f = open('../ptbdb/RECORDS', 'r')
for line in f:
    rfile = '../ptbdb/' + line.strip();
    record = wfdb.rdheader(rfile)
    diagnoses = rutil.extratPatientDiagnoses(record)
    for diagnosis in diagnoses:
        if not any(diagnosis in s for s in possible):
            possible.append(diagnosis)

print(possible)


#let's try to figure out what the best 'window' is to capture a single hearbeat
record = wfdb.rdsamp('../ptbdb/patient002/s0015lre')
print("the number of datapoint is %d "  % record.siglen)
nsig = record.nsig
plt.figure(1)
ncol = 2
nrow = round(nsig / 2.0)

for i in range(nsig):
    data = rutil.extractGraph(i, record)
    plt.subplot(nrow, ncol, i + 1)
    plt.title("lead " + record.signame[i])
    plt.plot(data[0:2000])
plt.show()
