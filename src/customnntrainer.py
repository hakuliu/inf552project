import wfdb
import recordTranslator as rutil
import numpy as np

class EcgTrainer:
    def __init__(self, recordlist, feedforward, diagnoses, inres, testList=None):
        self.trainingList = recordlist
        self.ffn = feedforward
        self.diagnoses = diagnoses
        self.testList = testList
        self.inres = inres

    def train(self, epochs):
        for i in range(epochs):
            print('training epoch %d' % i)
            self.trainSingleEpoch()
            if self.testList:
                print('testing epoch %d' % i)
                self.testSingleEpoch()

    def testSingleEpoch(self):
        self.test(self.testList)

    def test(self, data):
        pass

    def trainSingleEpoch(self):
        for rec in self.trainingList:
            print('training on ' + rec)
            record = wfdb.rdsamp('../ptbdb/'+rec)
            self.trainSingleRecord(record)

    def trainSingleRecord(self, record):
        self.ffn.stageInputs(self.prepareInputs(record))
        self.ffn.feedforward()
        self.ffn.stageErrors(self.prepareErrors(record))
        self.ffn.backPropagate()
        self.ffn.updateWeights()

    def prepareInputs(self, record):
        result = []
        for i in range(record.nsig):
            data = rutil.extractGraph(i, record)
            result.extend(data[0:self.inres])
        return result

    def prepareErrors(self, record):
         result = np.zeros(len(self.diagnoses))
         d = rutil.extratPatientDiagnoses(record)
         index = self.diagnoses.index(d)
         print('...has ' + d + ', ' + str(index))
         result[index] = 1.
         return result
