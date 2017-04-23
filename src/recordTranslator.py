'''
This package serves to provide a bunch of utility files that allows us to take samples read via our library
into data that is more convenient for our analysis, and easier for us to understand.
'''

def extractPatientAttributes(recordheader):
    '''
    uses the comments section(?) of the record to parse out relevant information
    that will be used for our learning algorithm (don't know if it'll be input or output yet)
    :param record: sample record read from wfdb.rdsamp
    :return: a dictionary of attribute - value
    '''
    attr = []
    comments = recordheader.comments
    for comment in comments:
        if comment.strip().startswith('Smoker'):
            attr.extend(comment.split(':')[1].split(','))
        if comment.strip().startswith('age'):
            attr.extend(comment.split(':')[1].split(','))
        if comment.strip().startswith('sex'):
            attr.extend(comment.split(':')[1].split(','))

    attr = map(str.strip, attr)

    return attr

def extratPatientDiagnoses(recordheader):
    '''
    parses the comments section(?) of the record to find out what kind of heart problem (if any) this patient had
    :param record: sample record read from wfdb.rdsamp
    :return: a list of diagnoses pertaining to this patient
    '''
    diag = []
    comments = recordheader.comments
    for comment in comments:
        if 'Reason for admission' in comment:# or 'Additional diagnoses' in comment:
            diag.extend(comment.split(':')[1].split(','))
    diag = map(str.strip, diag)

    for i in range(len(diag)):
        if('Healthy' in diag[i] or 'n/a' in diag[i]):
            diag[i] = 'Healthy'

    return diag

def extractAllGraphs(record):
    '''
    gets the entire graph data from the record
    :param record: 
    :return: 
    '''
    return record.p_signals

def extractGraph(index, record):
    '''
    gets a specific graph from all the graphs.
    It looks like the ECG data we have has 15 plots.
    These represent the electric signals read from patches attached to various parts of the patient's body.
    :param index: 
    :param record: 
    :return: 
    '''
    return extractAllGraphs(record)[:, index]