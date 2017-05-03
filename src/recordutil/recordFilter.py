import recordTranslator as rutil
import recordManager as rman
import wfdb
import numpy
import random
import matplotlib.pyplot as plot

RANDMIN = .1
RANDMAX = .9
WINDOWSIZE = 50
SEARCHSIZE = 5000
GAUSSIZE = 21

SEARCHSPIKE = 0
SEARCHZERO = 1
VARTHRESH = .08

def normalizeData(record, heartbeats=2, resolution=500):

    result = []
    totalVar = 1
    for t in range(20):
        result = []
        seed = random.triangular(RANDMIN, RANDMAX, RANDMIN + (RANDMAX - RANDMIN) / 2)
        (start, end) = getStartEndHeartbeats(record, seed, heartbeats=heartbeats)
        if start == end: continue
        for i in range(record.nsig):
            result.append(getARandomStandardizedData(rutil.extractGraph(i, record), resolution, start, end))
        totalVar = getTotalVariance(result)
        # print('try %d, var %.5f' % (t, totalVar))
        if totalVar < VARTHRESH:
            break


    # plot.figure()
    # plot.title(rutil.extratPatientDiagnoses(record))
    # plot.plot(result[1])
    # plot.show()

    return result

def getTotalVariance(allGraphs):
    variances = []
    for g in allGraphs:
        variances.append(numpy.var(g))
    return numpy.mean(variances)

def getARandomStandardizedData(data, resolution, start, end):
    increment = float(end - start) / resolution
    result = numpy.zeros(resolution)
    for i in range(resolution):
        index = start + i * increment
        result[i] = averageData(data, index)
    return result

def averageData(data, x):
    try:
        start = int(x - GAUSSIZE / 2)
        s = []
        for i in range(GAUSSIZE):
            s.append(data[start + i])
        return numpy.mean(s)
    except:
        return 0

def getStartEndHeartbeats(record, seed, heartbeats=2):
    variances = getVariances(record, seed)
    ma = max(variances)
    mi = min(variances)
    maxthresh = mi + (ma - mi) * .5
    minthresh = mi + (ma - mi) * .2

    state = SEARCHSPIKE
    firstPeak = 0
    lastPeak = -1
    beatLens = []

    for i in range(len(variances)):
        v = variances[i]
        if state == SEARCHSPIKE and v > maxthresh:
            state = SEARCHZERO
        elif state == SEARCHZERO and v < minthresh:
            state = SEARCHSPIKE
            if lastPeak > 0:
                beatLens.append(i - lastPeak)
            else:
                firstPeak = i
            lastPeak = i
    if(len(beatLens) == 0) :
        return (seed, 500*heartbeats)
    av = numpy.mean(beatLens)
    start = firstPeak - (av / 2)
    end = start + heartbeats * av
    return (start,end)


def getVariance(data):
    return numpy.var(data)

def getVariances(record, seed):

    datalen = record.siglen
    startIndex = int(datalen * seed)

    varians = numpy.zeros(SEARCHSIZE)

    for i in range(SEARCHSIZE):
        start = startIndex + i - WINDOWSIZE / 2
        end = start + WINDOWSIZE
        variantlist = []
        for g in range(15):
            x = getVariance(rutil.extractGraph(g, record)[start:end])
            variantlist.append(x)
        varians[i] = numpy.mean(variantlist)

    # ma = max(varians)
    # mi = min(varians)
    # maxthresh = mi + (ma - mi) * .5
    #
    # m = numpy.ones(len(varians))
    # m = maxthresh * m
    # plot.figure()
    # plot.plot(varians)
    # plot.plot(m)
    # plot.show()

    return varians

def saveStandardizedData():
    allrecords = rman.getIterableRecords(recordsFile='../../out/trainRecords')
    allrecords.extend(rman.getIterableRecords(recordsFile='../../out/testRecords'))
    for r in allrecords:
        saveOneData(r)

def saveOneData(r):
    outfile = open('../../out/standardized-data/' + r.replace('/', '-') + ".txt", 'w')
    record = wfdb.rdsamp('../../ptbdb/' + r)
    normalizeddata = normalizeData(record, heartbeats=4)
    for lead in normalizeddata:
        for i,val in enumerate(lead):
            outfile.write(str(val))
            if i != len(lead) - 1:
                outfile.write(',')
        outfile.write('\n')
    outfile.close()

def loadOneData(r):
    f = open('../../out/standardized-data/' + r.replace('/', '-') + ".txt", 'r')
    data = []
    for line in f:
        l = line.strip().split(',')
        fl = [float(x) for x in l]
        data.append(fl)
    plot.figure()
    plot.plot(data[2])
    plot.show()

def analyzeAllRecords():
    allrecords = rman.getIterableRecords(recordsFile='../../out/trainRecords')

    for r in allrecords:
        record = wfdb.rdsamp('../../ptbdb/' + r)
        normalizeddata = normalizeData(record, heartbeats=4)
        # print(r + ":")
        # print 'start: %d, end %d', (start, end)
        # if (start != end):
        #     rutil.showGraph(record, start, end)

#analyzeAllRecords()

saveStandardizedData()
