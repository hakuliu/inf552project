import recordTranslator as rutil
import recordManager as rman
import wfdb
import numpy
import matplotlib.pyplot as plot

PRIMARYLEAD = 12 #represent the first Frank Lead
STARTPERCENT = .3 #Don't want to start from 0. because the initial signals might be noisy
WINDOWSIZE = 400
SEARCHSIZE = 3000
GAUSSIZE = 15
ZEROTHRESH = 0.005
SPIKETHRESH = 0.01

SEARCHSPIKE = 0
SEARCHZERO = 1

def normalizeData(record, heartbeats=2, resolution=500):
    (start, end) = getStartEndHeartbeats(record, heartbeats=heartbeats)
    result = []
    for i in range(record.nsig):
        result.append(getNormalizedData(rutil.extractGraph(i, record), resolution, start, end))

    # plot.figure()
    # plot.plot(result[12])
    # plot.show()

    return result

def getNormalizedData(data, resolution, start, end):
    increment = float(end - start) / resolution
    result = numpy.zeros(resolution)
    for i in range(resolution):
        index = start + i * increment
        result[i] = averageData(data, index)
    return result

def averageData(data, x):
    start = int(x - GAUSSIZE / 2)
    s = []
    for i in range(GAUSSIZE):
        s.append(data[start + i])
    return sum(s) / GAUSSIZE

def getStartEndHeartbeats(record, heartbeats=2):
    vars = getVariances(record)
    state = SEARCHZERO
    beatfound = 0
    firstZero = -1
    for i in range(len(vars)):
        v = vars[i]
        if firstZero == -1:
            if v < ZEROTHRESH:
                firstZero = i
                state = SEARCHSPIKE
        else:
            if state == SEARCHSPIKE and v > SPIKETHRESH:
                state = SEARCHZERO
            elif state == SEARCHZERO and v < ZEROTHRESH:
                state = SEARCHSPIKE
                beatfound += 1
        if beatfound >= heartbeats:
            return (firstZero, i)
    return (0,0)


def getVariance(data):
    return numpy.var(data)

def getVariances(record):

    datalen = record.siglen
    startIndex = int(datalen * STARTPERCENT)
    xData = rutil.extractGraph(12, record)
    yData = rutil.extractGraph(13, record)
    zData = rutil.extractGraph(14, record)

    vars = numpy.zeros(SEARCHSIZE)

    for i in range(SEARCHSIZE):
        start = startIndex + i
        end = start + WINDOWSIZE
        x = getVariance(xData[start:end])
        y = getVariance(yData[start:end])
        z = getVariance(zData[start:end])
        vars[i] = sum([x,y,z]) / 3.

    # plot.figure()
    # plot.plot(vars)
    # plot.show()

    return vars

def analyzeAllRecords():
    allrecords = rman.getIterableTestRecords(recordsFile='../../ptbdb/RECORDS')
    # for r in allrecords:
    #     vars = getVariances(r)
    #     print(r + ":")
    #     print 'minvar was %.9f' % min(vars)
    #     print 'maxvar was %.9f' % max(vars)

    for r in allrecords:
        record = wfdb.rdsamp('../../ptbdb/' + r)
        normalizeddata = normalizeData(record)
        # print(r + ":")
        # print 'start: %d, end %d', (start, end)
        # if (start != end):
        #     rutil.showGraph(record, start, end)

#analyzeAllRecords()