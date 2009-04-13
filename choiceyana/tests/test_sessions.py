#!/bin/env python
''' Test Session class '''

from choiceyana.sessions import Session
from choiceyana.trials import Trial

def test_session():
    s = Session([])
    assert s.subject is None
    assert s.session is None
    L = list(s)
    assert L == []
    s = Session([None], '21', 2)
    assert s.subject == '21'
    assert s.session == 2
    L = list(s)
    assert L == [None]

def test_update():
    t1 = Trial({'test':'value'})
    t2 = Trial({'test2':'value2'})
    t3 = Trial()
    s1 = Session([t1])
    s2 = Session([t2, t3])
    s1.update_trials(s2)
    L = list(s1)
    assert L[0].rowdict == {'test':'value','test2':'value2'}

def test_ordering():
    t1 = Trial()
    t1.type = 'Rest'
    t2 = Trial()
    t2.type = 'Choice'
    s1 = Session([t1, t2])
    s2 = Session([t1, t2])
    assert s1.match_no(s2) == 2
    assert s2.match_no(s1) == 2
    s2 = Session([t1, t1])
    assert s1.match_no(s2) is None
    assert s2.match_no(s1) is None
    s2 = Session([t1])
    assert s1.match_no(s2) == 1
    assert s2.match_no(s1) == 1
    s3 = Session([])
    assert s1.match_no(s3) == 0
    assert s3.match_no(s1) == 0
    bm = s1.best_match([s2, s3])
    assert bm is s2
    bm = s1.best_match([])
    assert bm is None
    
