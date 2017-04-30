import numpy

def separateRecords(recordsFile='../ptbdb/RECORDS', outTraining='../out/trainRecords', outTesting='../out/testRecords', ratio=.75):
    '''
    In order to make sure we do not overfit the problem, we need to use a test set that is outside of our training set.
    Usually, to do this, we take our data, and divide it such that some of it is used for training and some for testing
    :return: 
    '''
    recFile = open(recordsFile, 'r')
    #We could do 1 pass to figure out how many records there are, and then another pass for actually separating...
    #But since we dont' expect the file to be that big, we'll just load it all in memory
    recordPaths = []
    print('reading records file...')
    for line in recFile:
        recordPaths.append(line.strip() + '\n')
    print('there were a total of %d records' % len(recordPaths))
    split = int(ratio * len(recordPaths))
    trainSet = recordPaths[:split]
    testSet = recordPaths[split:]
    print('the training set will be %d records' % len(trainSet))
    print('the test set will be %d records' % len(testSet))
    print('writing files...')
    o = open(outTraining, 'w')
    o.writelines(trainSet)
    o = open(outTesting, 'w')
    o.writelines(testSet)
    print('done.')

def getIterableTrainingRecords(recordsFile='../out/trainRecords'):
    return getIterableRecords(recordsFile)

def getIterableRecords(recordsFile='../ptbdb/RECORDS'):
    f = open(recordsFile, 'r')
    result = []
    for line in f:
        result.append(line.strip())
    return result

def getIterableTestRecords(recordsFile='../out/testRecords'):
    return getIterableRecords(recordsFile)

def getAllDiagnosis():
    d_f = open('../out/possible-diagnoses.txt', 'r')
    result = []
    for line in d_f:
        result.append(line.strip())
    return result