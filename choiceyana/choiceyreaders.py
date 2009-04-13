#!/bin/env python
''' Choiceyreaders return trial iterators '''

from choiceyana import readers
from choiceyana.choiceydefs import choicey_circles
from choiceyana.trials import Trial
from choiceyana.sessions import Session

def process_onoffs(instr):
    if not instr:
        return
    instr = instr.replace('{', ' ')
    instr = instr.replace('}', ' ')
    vals = instr.split()
    results = []
    for val in vals:
        if val == '1':
            results.append('on')
        elif val == '-1':
            results.append('off')
        else:
            results.append(None)
    return results

# Decorator to return None for unconvertable values
def intnone(instr):
    try:
        return int(instr)
    except ValueError:
        pass

def boolnone(instr):
    res = intnone(instr)
    if not res is None:
        return bool(res)
    
class ChoiceyReader(readers.FileReader):
    def _rowparse(self, row):
        rowd = super(ChoiceyReader, self)._rowparse(row)
        return Trial(rowd)


class EdataReader(ChoiceyReader):
    circles = choicey_circles
    importers = [
        ['Subject', str], 
        ['Session', intnone], 
        ['Trial', intnone], 
        ['Delay', intnone], 
        ['Hit', intnone], 
        ['PostFix.RESP', process_onoffs], 
        ['PreX', intnone], 
        ['PreY', intnone], 
        ['Ready', intnone], 
        ['T1', intnone], 
        ['T2', intnone], 
        ['T3', intnone], 
        ['Target', intnone], 
        ['TrialType', str], 
        ['Valid', intnone], 
        ['X1', intnone], 
        ['X2', intnone], 
        ['X3', intnone], 
        ['Y1', intnone], 
        ['Y2', intnone], 
        ['Y3', intnone], 
        ['OffStart', intnone], 
        ]

    def _rowparse(self, row):
        trial = super(EdataReader, self)._rowparse(row)
        trial.type = trial.rowdict['TrialType']
        return trial
    
    @property
    def sessions(self):
        try:
            return self._sessions
        except AttributeError:
            pass
        sessions = {}
        for row in self.rows:
            rowd = row.rowdict
            sess_id = (rowd['Subject'],rowd['Session'])
            if not sessions.has_key(sess_id):
                sessions[sess_id] = []
            sessions[sess_id].append(row)
        sess_list = []
        for sess_id in sessions:
            sess_list.append(Session(sessions[sess_id], *sess_id))
        self._sessions = sess_list
        return self._sessions

    @property
    def subjects(self):
        subjects = {}
        for sess in self.sessions:
            subject = sess.subject
            if not subjects.has_key(subject):
                subjects[subject] = []
            subjects[subject].append(sess)
        return subjects

            
class OrderReader(ChoiceyReader, Session):
    default_dialect = 'excel-tab'
    importers = [
        ['Weight', intnone],
        ['Nested', intnone],
        ['Procedure', str],
        ['TrialType', str],
        ['Task', intnone],
        ['C1', str],
        ['C2', str],
        ['C3', str],
        ['C4', str],
        ['Fix', str],
        ['Target', str],
        ['Good', str]]

    def __init__(self, fileobj):
        super(OrderReader, self).__init__(fileobj)
        self.subject = None
        self.session = None
        
    def _rowparse(self, row):
        trial = super(OrderReader, self)._rowparse(row)
        trial.type = trial.rowdict['TrialType']
        return trial

dat_trial_decode = {
    '0':'Rest',
    '1':'Choice',
    '2':'Direct2',
    '3':'Symbolic',
    '4': 'Direct4'}

def dattrialcode(instr):
    try:
        return dat_trial_decode[instr]
    except KeyError:
        return None

class DatReader(ChoiceyReader, Session):
    default_dialect = 'excel-tab'
    cols_first = False
    '''
    TargetRecoded is the desired target for non-choice trials. For
    choice trials, it is the target (of the two desired targets), that
    you were closest to. A value of 5 means that this is a choice
    condition and the response was exactly midway between the two
    potiential choices
    '''
    importers = [
        ['TrialCode', dattrialcode],
        ['TargetRecoded', intnone],
        ['Ready', boolnone],
        ['Hit', boolnone],
        ['ReadyOnset', intnone],
        ['ReadyOffset', intnone],
        ['GoOnset', intnone],
        ['GoOffset', intnone],
        ['FBOnset', intnone],
        ['FBOffset', intnone],
        ['TTLTimePre', intnone],
        ['TTLTimePost', intnone]]

    def __init__(self, fileobj, subject=None, session=None):
        super(DatReader, self).__init__(fileobj)
        self.subject = subject
        self.session = session

    def _rowparse(self, row):
        trial = super(DatReader, self)._rowparse(row)
        trial.type = trial.rowdict['TrialCode']
        return trial
