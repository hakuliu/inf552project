import math

import numpy as np
import wfdb

import src.recordutil.recordTranslator as rutil


class EcgTrainer:
    def __init__(self, recordlist, feedforward, diagnoses, inres, testList=None):
        self.trainingList = recordlist
        self.ffn = feedforward
        self.diagnoses = diagnoses
        self.testList = testList
        self.inres = inres
        if testList:
            self.testfile = open('../out/feedforwardtest.csv', 'w')

    def train(self, epochs):
        for i in range(epochs):
            print('training epoch %d' % i)
            self.trainSingleEpoch()
            if self.testList:
                print('testing epoch %d' % i)
                self.testSingleEpoch(i)

    def testSingleEpoch(self, i):
        ers = []
        numcorrect = 0
        for rec in self.testList:
            print('testing ' + rec)
            record = wfdb.rdsamp('../ptbdb/'+rec)
            (sqerr, correct) = self.error(record)
            ers.append(sqerr)
            if correct: numcorrect += 1
        totalsqerr = math.sqrt(sum(ers))
        correctpercent = float(numcorrect) / len(self.testList)
        self.testfile.write(str(i) + "," + str(totalsqerr) + "," + str(correctpercent) + "\n")


    def trainSingleEpoch(self):
        for rec in self.trainingList:
            print('training on ' + rec)
            record = wfdb.rdsamp('../ptbdb/'+rec)
            self.trainSingleRecord(record)

    def trainSingleRecord(self, record):
        self.ffn.stageInputs(self.prepareInputs(record))
        self.ffn.feedforward()
        self.ffn.stageErrors(self.getResult(record)[0])
        self.ffn.backPropagate()
        self.ffn.updateWeights()

    def prepareInputs(self, record):
        result = []
        for i in range(record.nsig):
            data = rutil.extractGraph(i, record)
            result.extend(data[0:self.inres])
        return result

    def getResult(self, record):
         result = np.zeros(len(self.diagnoses))
         d = rutil.extratPatientDiagnoses(record)
         index = self.diagnoses.index(d)
         print('...has ' + d + ', ' + str(index))
         result[index] = 1.
         return (result, index)

    def error(self, record):
        self.ffn.stageInputs(self.prepareInputs(record))
        self.ffn.feedforward()
        (resArray, resIndex) = self.getResult(record)
        predictIndex = self.getFFNLargestOut()
        print('Prediction was %d' % predictIndex)
        print('Real result was %d' % resIndex)
        resultCorrect = resIndex == predictIndex
        sqerr = self.getFFNSquaredError(resArray)

        return (sqerr, resultCorrect)

    def getFFNSquaredError(self, resultArray):
        sqerrs = []
        for i in range(len(self.ffn.outnodes)):
            nodex = self.ffn.outnodes[i].x
            res = resultArray[i]

            sqerrs.append((nodex - res) ** 2)
        return sum(sqerrs)

    def getFFNLargestOut(self):
        maxVal = 0
        maxInd = 0
        for i in range(len(self.ffn.outnodes)):
            node = self.ffn.outnodes[i]
            if node.x > maxVal:
                maxVal = node.x
                maxInd = i
        return maxInd


