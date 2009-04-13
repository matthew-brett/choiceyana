#!/bin/env python
''' Test readers '''

import os
from StringIO import StringIO

import nose

from choiceyana.readers import FileReader

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

def test_reader():
    fobj = StringIO(test_data)
    rdr = FileReader(fobj)
    rdr.importers = test_importers
    # Is it iterable?
    for row in rdr:
        assert isinstance(row, dict)
    assert row['Number2'] == 4
    assert row['String2'] == 'test_once_more'
    assert rdr.columns == ['String1', 'Number1', 'Number2', 'String2']
    # Can I make a list?
    rows = list(rdr)
    # Can I get the data again?
    rows = rdr.rows
    # Can I tell the reader not to omit the first row?
    fobj.seek(0)
    lines = fobj.readlines()
    not_first = '\n'.join(lines[1:])
    fobj = StringIO(not_first)
    rdr = FileReader(fobj)
    rdr.importers = test_importers
    rdr.cols_first = False
    rows = list(rdr)
    assert rows[0]['Number2'] == 3
    assert rows[0]['String2'] == 'test_again'
    assert rows[-1]['Number2'] == 4
    assert rows[-1]['String2'] == 'test_once_more'
    assert rdr.columns == []
    
