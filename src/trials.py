'''
We perform various different experiment to see what graph architecture, 
what data used, etc. would do the best in learning. Each configurations are
contained within a function here.
'''
import hw5.feedforward as ff
from src.recordutil import recordManager as records
from src.trainers import customnntrainer as fft

NUM_GRAPHS = 15

def trialFullFeedForward():
    trainFiles = records.getIterableTrainingRecords()
    testFiles = records.getIterableTrainingRecords()
    diagnoses = records.getAllDiagnosis()

    in_resolution = 800
    useGraph = [12,13,14]
    hidden = [500]

    ffn = ff.FeedForwardNetwork(len(useGraph) * in_resolution, len(diagnoses) + 1, hidden)
    ffn.constructNetwork()
    trainer = fft.EcgTrainer(trainFiles[317:319], ffn, diagnoses, in_resolution, useGraph, testList=testFiles[317:319])
    trainer.train(3000)

trialFullFeedForward()