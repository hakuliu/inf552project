'''
This package serves to provide a bunch of utility files that allows us to take samples read via our library
into data that is more convenient for our analysis, and easier for us to understand.
'''

def extractPatientAttributes(record):
    '''
    uses the comments section(?) of the record to parse out relevant information
    that will be used for our learning algorithm (don't know if it'll be input or output yet)
    :param record: sample record read from wfdb.rdsamp
    :return: a dictionary of attribute - value
    '''
    return None

def extratPatientDiagnoses(record):
    '''
    parses the comments section(?) of the record to find out what kind of heart problem (if any) this patient had
    :param record: sample record read from wfdb.rdsamp
    :return: a list of diagnoses pertaining to this patient
    '''
    return None

def extractAllGraphs(record):
    '''
    gets the entire graph data from the record
    :param record: 
    :return: 
    '''
    return None

def extractGraph(index, record):
    '''
    gets a specific graph from all the graphs.
    It looks like the ECG data we have has 15 plots.
    These represent the electric signals read from patches attached to various parts of the patient's body.
    :param index: 
    :param record: 
    :return: 
    '''
    return None