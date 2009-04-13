#!/bin/env python
''' Test choicey readers '''

import os
from StringIO import StringIO

import choiceyana.choiceyreaders as cacr
from choiceyana.trials import Trial

datapath, _ = os.path.split(__file__)
datapath = os.path.join(datapath, 'data')
order1fname = os.path.join(datapath, 'order_example1.txt')
order2fname = os.path.join(datapath, 'order_example2.txt')
order3fname = os.path.join(datapath, 'order_example3.txt')
datfname = os.path.join(datapath, 'dat_example1.txt')
edatafname = os.path.join(datapath, 'edata_example.txt')

def test_process_ononffs():
    func = cacr.process_onoffs
    assert func('1') == ['on']
    assert func('-1') == ['off']
    assert func('{-1}1') == ['off', 'on']
    assert func('{-1}1{-1}') == ['off', 'on', 'off']
    assert func('{1}-1{1}') == ['on', 'off', 'on']
    assert func('B') == [None]

def test_ornones():
    assert cacr.intnone('1') == 1
    assert cacr.intnone('B') is None
    assert cacr.boolnone('1') is True
    assert cacr.boolnone('0') is False
    assert cacr.boolnone('B') is None
    
test_data = \
'''String1,Number1,Number2,String2
test1,1,3,test_again
test2,10,4,test_once_more
'''
test_importers = [
    ['String1', str],
    ['Number1', int],
    ['Number2', int],
    ['String2', str]]

def test_choiceyreader():
    fobj = StringIO(test_data)
    rdr = cacr.ChoiceyReader(fobj)
    rdr.importers = test_importers
    rows = list(rdr)
    assert isinstance(rows[0], Trial)

def test_orderreader():
    rdr = cacr.OrderReader(file(order1fname, 'rt'))
    rows = list(rdr)
    assert rows[0].type == 'Rest'
    assert rows[-1].type == 'Direct4'

def test_dattrialcode():
    func = cacr.dattrialcode
    assert func('0') == 'Rest'
    assert func('1') == 'Choice'
    assert func('2') == 'Direct2'
    assert func('3') == 'Symbolic'
    assert func('4') == 'Direct4'
    assert func(4) is None

def test_datreader():
    rdr = cacr.DatReader(file(datfname, 'rt'))
    assert rdr.cols_first is False
    assert rdr.columns == []
    rows = list(rdr)
    assert rows[0].type == 'Choice'
    assert rows[-1].type == 'Direct4'

def test_edatareader():
    rdr = cacr.EdataReader(file(edatafname, 'rt'))
    rows = list(rdr)
    rows[0].type == 'Choice'
    rows[-1].type == 'Rest'
    sesses = list(rdr.sessions)
    assert len(sesses) == 2
    subjects = rdr.subjects
    assert len(subjects.keys()) == 1

def test_ordering_data():
    rdr = cacr.EdataReader(file(edatafname, 'rt'))
    sessions = rdr.sessions
    drdr = cacr.DatReader(file(datfname, 'rt'))
    ordr1 = cacr.OrderReader(file(order1fname, 'rt'))
    ordr2 = cacr.OrderReader(file(order2fname, 'rt'))
    ordr3 = cacr.OrderReader(file(order3fname, 'rt'))
    mno = sessions[0].match_no(drdr)
    assert mno == 120
    mno = sessions[1].match_no(drdr)
    assert mno is None
    mno = sessions[0].match_no(ordr1)
    assert mno is None
    mno = sessions[0].match_no(ordr2)
    assert mno is None
    mno = sessions[1].match_no(ordr1)
    assert mno is None
    mno = sessions[1].match_no(ordr2)
    assert mno == 120
    sessions[0].update_trials(drdr, ordr3)
    sessions[1].update_trials(ordr2)
    for tno, trial in enumerate(sessions[0]):
        if not trial.isrest:
            if trial.RTMT > 1000:
                print tno, trial.RT, trial.MT, trial.outcome
            
