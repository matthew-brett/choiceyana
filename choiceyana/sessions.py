#!/bin/env python
''' Session class for containing trials
'''
import itertools

class Session(object):
    ''' Session iterator with subject and session ids '''
    def __init__(self, iterable, subject=None, session=None):
        self.iterable = iterable
        self.subject = subject
        self.session = session

    def __iter__(self):
        return iter(self.iterable)

    def match_no(self, another, matcher=None):
        ''' Test if two sessions have the same order
        Returns number of matches, or None if there
        are any non-matching entries
        '''
        if matcher is None:
            matcher = lambda x, y:x.type==y.type
        L1 = list(self)
        L2 = list(another)
        if not len(L1) or not len(L2):
            return 0
        if len(L1) < len(L2):
            shorter = L1
            longer = L2
        else:
            shorter = L2
            longer = L1
        ilonger = iter(longer)
        nmatch = 0
        for val in shorter:
            val2 = ilonger.next()
            if not matcher(val, val2):
                return None
            nmatch += 1
        return nmatch

    def best_match(self, matches, matcher=None):
        matches = list(matches)
        if len(matches) == 0:
            return None
        res = None
        best = None
        for match in matches:
            mno = self.match_no(match, matcher=matcher)
            if mno is None:
                continue
            if best is None or mno > best:
                res = match
                best = mno
        return res

    def update_trials(self, *args):
        ''' Update trials from other sessions in args '''
        other_sesses = itertools.izip(*args)
        for trial in self:
            trial.update(*other_sesses.next())

    def apply_trials(self, trial_method, *args, **kwargs):
        for trial in self:
            trial_method(self, *args, **kwargs)
        
    
