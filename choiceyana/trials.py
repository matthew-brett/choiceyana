#!/bin/env python
''' Trial and trial analysis '''

from functools import wraps

import choiceydefs

class NAPrinter(type):
    'Metaclass to allow UnknownValue to pretty print '''
    def __str__(self):
        return 'NA'
    
class UnknownValue(object):
    __metaclass__ = NAPrinter
    
class TouchEvent(object):
    ''' Class to contain touch screen events '''
    def __init__(self, time=None, circle=None, onoff=None):
        self.time = time
        self.circle = circle
        self.onoff = onoff

class TouchEventCollection(object):
    ''' Collection of TouchEvents '''
    circles = choiceydefs.choicey_circles
    target_names = choiceydefs.target_names
    def __init__(self, events):
        self.events = events

    def append(self, event):
        self.events.append(event)

    def __iter__(self):
        return iter(self.events)

    def __len__(self):
        return len(self.events)
        
class Trial(object):
    ''' Class to contain trial information '''
    circles = choiceydefs.choicey_circles
    target_names = choiceydefs.target_names
    def __init__(self, rowdict=None):
        if rowdict is None:
            rowdict = {}
        self.cache = {}
        self.set_rowdict(rowdict)

    def get_rowdict(self):
        return self._rowdict
    def set_rowdict(self, rowdict):
        self._rowdict = rowdict
        self.events = self.gen_events()
        self.start_ok = self.gen_start_ok()
        self.pre_circle = self.gen_pre_circle()
        self.touched_target = self.gen_touched_target()
        self.stimuli = self.gen_stimuli()
    rowdict = property(get_rowdict, set_rowdict, None, 'row dictionary')

    def gen_pre_circle(self):
        try:
            prex = self.rowdict['PreX']
            prey = self.rowdict['PreY']
        except KeyError:
            return UnknownValue
        return self.circles.inside_which_name(prex, prey)

    def gen_events(self):
        try:
            resp_defs = self.rowdict['PostFix.RESP']
        except KeyError:
            return UnknownValue
        events = TouchEventCollection([])
        if not resp_defs:
            return events
        for i, resp_def in enumerate(resp_defs):
            event = TouchEvent(onoff=resp_def)
            time, X, Y = self._get_event_info(i)
            if not time is None:
                event.time = time
                event.circle = self.circles.inside_which_name(X, Y)
            events.append(event)
        return events
        
    def gen_start_ok(self):
        ''' We allow any trial where first event in is start circle
        In other words going into, or out of the start circle '''
        events = self.events
        if events is UnknownValue:
            return UnknownValue
        if not events:
            return False
        e1 = list(events)[0]
        return e1.circle == 'start'

    def gen_touched_target(self):
        events = self.events
        if events is UnknownValue:
            return UnknownValue
        for ev in events:
            if ev.onoff == 'on' and ev.circle in self.target_names:
                return ev.circle

    def gen_stimuli(self):
        ps = []
        for tno in range(1,5):
            fld = 'C%d' % tno
            try:
                target = self.rowdict[fld]
            except KeyError:
                return UnknownValue
            ps.append(target)
        try:
            fix = self.rowdict['Fix']
        except KeyError:
            return UnknownValue
        ps.append(fix)
        if len(ps) < 5:
            raise ValueError('Should have 5 stimuli')
        return ps

    @property
    def trialtype(self):
        try:
            return self.type
        except AttributeError:
            pass
        try:
            return self.rowdict['TrialType']
        except KeyError:
            return UnknownValue
        
    @property
    def correct_targets(self):
        stimuli = self.stimuli
        if stimuli is UnknownValue:
            return UnknownValue
        ttype = self.trialtype
        if ttype is UnknownValue:
            return UnknownValue
        gts = []
        if ttype == 'Choice':
            for i in range(4):
                if stimuli[i] == 'circle.bmp':
                    gts.append(self.target_names[i]) 
            return gts
        elif ttype in ('Direct2', 'Direct4'):
            for i in range(4):
                if stimuli[i] == 'direct.bmp':
                    gts.append(self.target_names[i])
            if len(gts) > 1:
                raise ValueError('More than one direct target')
            return gts
        elif ttype == 'Symbolic':
            # Correct target given by filename - eg 'sym2.bmp'
            fix = stimuli[-1]
            nstr = fix[3]
            n = int(nstr)
            return [self.target_names[n-1]]

    @property
    def outcome(self):
        ''' One of correct, incorrect, miss, or UnknownValue '''
        touched_target = self.touched_target
        if touched_target is UnknownValue:
            return UnknownValue
        correct_targets = self.correct_targets
        if correct_targets is UnknownValue:
            return UnknownValue
        if touched_target is None:
            return 'miss'
        if touched_target in correct_targets:
            return 'correct'
        else:
            return 'incorrect'

    @property
    def RT(self):
        ''' RT can conly be calculated if the first event was at start
        If the first event was start 'off' then RT is the time of this 'off'
        If the first event was start 'on', and the second event was
        start 'off', then the RT is the time of start 'off' '''
        start_ok = self.start_ok
        if start_ok is UnknownValue:
            return UnknownValue
        if not start_ok:
            return UnknownValue
        events = self.events
        if events is UnknownValue:
            return UnknownValue
        for ev in events:
            if ev.circle == 'start' and ev.onoff == 'off':
                break
        else:
            return UnknownValue
        # Might want to include OnsetDelay, not sure
        # Neil to check...
        return ev.time

    @property
    def MT(self):
        ''' MT can conly be calculated uniquely if we can get the RT
        and if they have hit a target '''
        RT = self.RT
        if RT is UnknownValue:
            return UnknownValue
        events = self.events
        for ev in events:
            if ev.circle in self.target_names and ev.onoff == 'on':
                break
        else:
            return UnknownValue
        return ev.time - RT

    @property
    def RTMT(self):
        ''' Combined RT and MT can be calculated even when RT and MT cannot
        when the first event was hitting the target '''
        events = self.events
        if events is UnknownValue or len(events) < 1:
            return UnknownValue
        events = list(events)
        if events[0].circle in self.target_names and events[0].onoff == 'on':
            return events[0].time
        RT = self.RT
        MT = self.MT
        if RT is UnknownValue or MT is UnknownValue:
            return UnknownValue
        return RT+MT

    def onset_duration(self, typestr):
        try:
            onset = self._rowdict[typestr + 'Onset']
        except KeyError:
            return UnknownValue
        try:
            offset = self._rowdict[typestr + 'Offset']
        except KeyError:
            return UnknownValue
        return onset, offset-onset
    
    @property
    def isrest(self):
        tt = self.trialtype
        if tt is UnknownValue:
            return UnknownValue
        return self.trialtype == 'Rest'

    def _get_event_info(self, eno):
        ''' Helper routine to get information for an event '''
        try:
            time, X, Y = [self.rowdict['%s%d' % (s, eno+1)]
                          for s in ('T', 'X', 'Y')]
        except KeyError:
            return [None]*3
        return time, X, Y

    @property
    def trialtype_consistent(self):
        pass
    
    def update(self, *args):
        rowd = self._rowdict
        for arg in args:
            rowd.update(arg.rowdict)
        self.rowdict = rowd
    

def trial_ref(trial):
    ''' Return string  appropriate for trial 
    event type (string), onset, duration, modulator
    '''
    res = []
    if trial.isrest:
        return res
    res.append('Ready\t%d\t%d' % trial.onset_duration('Ready'))
    tt = trial.trialtype
    gos = trial.onset_duration('Go')
    res.append('%s\t%d\t%d' % (tt, gos[0], gos[1]))
    res.append('FB\t%d\t%d' % trial.onset_duration('FB'))
    return res
