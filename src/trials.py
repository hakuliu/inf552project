'''
We perform various different experiment to see what graph architecture, 
what data used, etc. would do the best in learning. Each configurations are
contained within a function here.
'''
import recordManager as records
import hw5.feedforward as ff

def trialFullFeedForward():
    trainFiles = records.getIterableTrainingRecords()
    testFiles = records.getIterableTestRecords()
    diagnoses = records.getAllDiagnosis()

    ffn = ff.FeedForwardNetwork(7000, [4000, 1000], len(diagnoses))
    ffn.constructNetwork()


