'''
We perform various different experiment to see what graph architecture, 
what data used, etc. would do the best in learning. Each configurations are
contained within a function here.
'''
import recordManager as records
import hw5.feedforward as ff
import customnntrainer as fft

NUM_GRAPHS = 15

def trialFullFeedForward():
    trainFiles = records.getIterableTrainingRecords()
    testFiles = records.getIterableTestRecords()
    diagnoses = records.getAllDiagnosis()

    in_resolution = 500

    ffn = ff.FeedForwardNetwork(NUM_GRAPHS * in_resolution, len(diagnoses), [300])
    ffn.constructNetwork()
    trainer = fft.EcgTrainer(trainFiles[300:], ffn, diagnoses, in_resolution, testList=testFiles)
    trainer.train(20)



trialFullFeedForward()