#!/bin/env python

from StringIO import StringIO

from choiceyana.trials import Trial, UnknownValue, TouchEvent, \
     TouchEventCollection, trial_ref
from choiceyana.choiceyreaders import EdataReader, OrderReader, DatReader

edata_str = '''Subject","Session","Trial","Delay","Hit","PostFix.RESP","PreX","PreY","Ready","T1","T2","T3","Target","TrialType","Valid","X1","X2","X3","Y1","Y2","Y3","OffStart"
21,1,1,1764,1,"{-1}1{-1}",309,375,1,637,838,1060,1,"Choice",1,309,178,178,375,308,308,0
21,1,2,928,1,"{-1}1{-1}",313,382,1,440,684,882,3,"Direct4",1,313,379,379,382,215,215,0
21,1,7,2101,1,"1{-1}1",306,374,1,882,1057,1461,1,"Symbolic",1,192,192,306,315,315,372,1
21,1,8,1099,1,"{-1}1{-1}",306,372,1,542,768,937,2,"Direct2",1,306,263,263,372,220,220,0
'''
dat_str = '''1	1	1	1	34184	35952	35968	37868	37969	38369	0
4	3	1	1	38486	39421	39436	41336	41438	41838	0
3	1	1	1	57346	59448	59464	61364	61465	61865	0
2	2	1	1	61982	63084	63099	64999	65101	65501	0
'''
ord_str = '''Weight	Nested	Procedure	TrialType	Task	C1	C2	C3	C4	Fix	Target	Good
1		TrialProc	Choice	3	circle.bmp	circle.bmp	blank.bmp	blank.bmp	fix.bmp	5	Good Job.
1		TrialProc	Direct4	1	circle.bmp	circle.bmp	direct.bmp	circle.bmp	fix.bmp	3	Good Job.
1		TrialProc	Symbolic	4	circle.bmp	circle.bmp	circle.bmp	circle.bmp	sym1.bmp	1	Good Job.
1		TrialProc	Direct2	2	blank.bmp	direct.bmp	circle.bmp	blank.bmp	fix.bmp	2	Good Job.
'''

def test_tec():
    ''' Test TouchEventCollection '''
    tec = TouchEventCollection([])
    

def test_trial():
    t = Trial()
    assert t.rowdict == {}
    d = {'test':'value'}
    t = Trial(d)
    assert t.rowdict == d
    t = Trial(rowdict=d)
    assert t.rowdict == d
    d2 = {'test2':'value2'}
    t2 = Trial(rowdict=d2)
    t.update(t2)
    d.update(d2)
    assert t.rowdict == d

def test_fake_analysis():
    t = Trial()
    assert t.pre_circle is UnknownValue
    assert t.events is UnknownValue
    assert t.start_ok is UnknownValue
    assert t.pre_circle is UnknownValue
    assert t.touched_target is UnknownValue
    assert t.stimuli is UnknownValue
    assert t.trialtype is UnknownValue
    assert t.correct_targets is UnknownValue
    assert t.outcome is UnknownValue
    assert t.RT is UnknownValue
    assert t.MT is UnknownValue
    assert t.RTMT is UnknownValue
    startoff = TouchEvent(100, 'start', 'off')
    starton = TouchEvent(55, 'start', 'on')
    assert t.isrest is UnknownValue
    assert t.onset_duration('Ready') is UnknownValue
    assert t.onset_duration('Go') is UnknownValue
    assert t.onset_duration('FB') is UnknownValue
    
def test_real_analysis():
    erdri = iter(EdataReader(StringIO(edata_str)))
    drdri = iter(DatReader(StringIO(dat_str)))
    ordri = iter(OrderReader(StringIO(ord_str)))
    etrial = erdri.next()
    dtrial = drdri.next()
    otrial = ordri.next()
    etrial.update(dtrial)
    etrial.update(otrial)
    assert etrial.pre_circle == 'start'
    events = list(etrial.events)
    assert len(events) == 3
    assert etrial.start_ok is True
    assert etrial.pre_circle == 'start'
    assert etrial.touched_target == 't1'
    assert etrial.stimuli == [
        'circle.bmp',
        'circle.bmp',
        'blank.bmp',
        'blank.bmp',
        'fix.bmp',
        ]
    assert etrial.trialtype == 'Choice'
    assert etrial.correct_targets == ['t1', 't2']
    assert etrial.outcome == 'correct'
    assert etrial.RT == 637
    assert etrial.MT == 838 - etrial.RT
    assert etrial.RTMT == 838
    assert etrial.isrest is False
    assert etrial.onset_duration('Ready') == (34184, 35952-34184)
    assert etrial.onset_duration('Go') == (35968, 37868-35968)
    assert etrial.onset_duration('FB') == (37969, 38369-37969)
    
    
    # Another trial
    etrial = erdri.next()
    dtrial = drdri.next()
    otrial = ordri.next()
    etrial.update(dtrial)
    etrial.update(otrial)
    assert etrial.pre_circle == 'start'
    events = list(etrial.events)
    assert len(events) == 3
    assert etrial.start_ok is True
    assert etrial.pre_circle == 'start'
    assert etrial.touched_target == 't3'
    assert etrial.stimuli == [
        'circle.bmp',
        'circle.bmp',
        'direct.bmp',
        'circle.bmp',
        'fix.bmp',
        ]
    assert etrial.trialtype == 'Direct4'
    assert etrial.correct_targets == ['t3']
    assert etrial.outcome == 'correct'
    assert etrial.RT == 440
    assert etrial.MT == 684 - etrial.RT
    assert etrial.RTMT == 684
    
    # And another
    etrial = erdri.next()
    dtrial = drdri.next()
    otrial = ordri.next()
    etrial.update(dtrial)
    etrial.update(otrial)
    assert etrial.pre_circle == 'start'
    events = list(etrial.events)
    assert len(events) == 3
    assert etrial.start_ok is False
    assert etrial.pre_circle == 'start'
    assert etrial.touched_target == 't1'
    assert etrial.stimuli == [
        'circle.bmp',
        'circle.bmp',
        'circle.bmp',
        'circle.bmp',
        'sym1.bmp',
        ]
    assert etrial.trialtype == 'Symbolic'
    assert etrial.correct_targets == ['t1']
    assert etrial.outcome == 'correct'
    assert etrial.RT is UnknownValue
    assert etrial.RTMT == 882
    
    # And another
    etrial = erdri.next()
    dtrial = drdri.next()
    otrial = ordri.next()
    etrial.update(dtrial)
    etrial.update(otrial)
    assert etrial.pre_circle == 'start'
    events = list(etrial.events)
    assert len(events) == 3
    assert etrial.start_ok is True
    assert etrial.pre_circle == 'start'
    assert etrial.touched_target == 't2'
    assert etrial.stimuli == [
        'blank.bmp',
        'direct.bmp',
        'circle.bmp',
        'blank.bmp',
        'fix.bmp',
        ]
    assert etrial.trialtype == 'Direct2'
    assert etrial.correct_targets == ['t2']
    assert etrial.outcome == 'correct'
    assert etrial.RT == 542
    assert etrial.MT == 768 - etrial.RT
    assert etrial.RTMT == 768
    #print '\n'.join(trial_ref(etrial))
