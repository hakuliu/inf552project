import math
import random
import numpy as np
import wfdb

import src.recordutil.recordTranslator as rutil
import src.recordutil.recordFilter as filter

NUMHEARTBEATS = 2

class EcgTrainer:
    def __init__(self, recordlist, feedforward, diagnoses, inres, graphIndeces, testList=None):
        self.trainingList = recordlist
        self.ffn = feedforward
        self.diagnoses = diagnoses
        self.testList = testList
        self.inres = inres
        self.graphs = graphIndeces
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
        random.shuffle(self.testList)
        ers = []
        numcorrect = 0
        numHealthyCorrect = 0
        for rec in self.testList:
            #print('testing ' + rec)
            record = wfdb.rdsamp('../ptbdb/'+rec)
            (sqerr, correct, healthyCorrect) = self.error(record)
            ers.append(sqerr)
            if correct: numcorrect += 1
            if healthyCorrect: numHealthyCorrect += 1
        totalsqerr = math.sqrt(sum(ers))
        correctpercent = float(numcorrect) / len(self.testList)
        correctHealth = float(numHealthyCorrect) / len(self.testList)
        print('square mean error: %.4f' % totalsqerr)
        print('correct predictions: %.4f' % correctpercent)
        print('correct healthy prediction: %.4f' % correctHealth)
        self.testfile.write(str(i) + "," + str(totalsqerr) + "," + str(correctpercent) + "," + str(correctHealth) + "\n")


    def trainSingleEpoch(self):
        random.shuffle(self.trainingList)
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
        data = filter.normalizeData(record, NUMHEARTBEATS, self.inres)
        for i in self.graphs:
            result.extend(data[i])
        return result

    def getResult(self, record):
        totallen = len(self.diagnoses) + 1
        result = np.zeros(totallen)
        d = rutil.extratPatientDiagnoses(record)
        index = self.diagnoses.index(d)
        result[index] = 1.
        if 'Healthy' in d:
            result[totallen - 1] = 1
        return (result, index)

    def error(self, record):
        self.ffn.stageInputs(self.prepareInputs(record))
        self.ffn.feedforward()
        (resArray, resIndex) = self.getResult(record)
        predictIndex = self.getFFNLargestOut()
        resultCorrect = resIndex == predictIndex
        sqerr = self.getFFNSquaredError(resArray)
        healthy = self.getHealthyPrediction()
        healthyCorrect = resArray[-1] == healthy

        return (sqerr, resultCorrect, healthyCorrect)

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
        for i in range(len(self.ffn.outnodes) - 1):
            node = self.ffn.outnodes[i]
            if node.x > maxVal:
                maxVal = node.x
                maxInd = i
        return maxInd

    def getHealthyPrediction(self):
        if self.ffn.outnodes[-1].x >= .5: return 1
        else: return 0
