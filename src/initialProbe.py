import matplotlib.pyplot as plt
import wfdb

from src.recordutil import recordTranslator as rutil


def writeAllDiagnosisToFile():
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

    diagnosesfile = open('../out/possible-diagnoses.txt', 'w')
    for d in possible:
        diagnosesfile.write(d + '\n')



#let's try to figure out what the best 'window' is to capture a single hearbeat
def showGraph(pat='patient002/s0015lre'):
    record = wfdb.rdsamp('../ptbdb/'+pat)
    print("the number of datapoint is %d "  % record.siglen)
    nsig = record.nsig
    plt.figure(1)
    ncol = 2
    nrow = round(nsig / 2.0)

    for i in range(nsig):
        data = rutil.extractGraph(i, record)
        plt.subplot(nrow, ncol, i + 1)
        plt.title("lead " + record.signame[i])
        plt.plot(data[3000:5000])
    plt.show()

def writePatientData():
    f = open('../ptbdb/RECORDS', 'r')
    o = open('../out/patientAttr.txt', 'w')
    for line in f:
        pat = line.strip()
        rfile = '../ptbdb/' + pat;
        record = wfdb.rdheader(rfile)
        diagnoses = rutil.extratPatientDiagnoses(record)
        attributes = rutil.extractPatientAttributes(record)
        o.write(pat)
        o.write(',')
        o.write(rfile)
        for attr in attributes:
            o.write(',')
            o.write(attr)
        o.write(',')
        o.write(diagnoses[0])
        o.write('\n')

showGraph(pat='patient002/s0015lre')