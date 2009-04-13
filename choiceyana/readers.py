#!/bin/env python
''' File readers return row iterators, where rows are dictionaries of values '''

import csv

class FileReader(object):
    ''' Class to read data from files using converters '''
    importers = None
    default_dialect = 'excel'
    cols_first = True
    def __init__(self, fileobj, dialect=None):
        if dialect is None:
            dialect = self.default_dialect
        self.fileobj = fileobj
        self.dialect = dialect
        self._rows = []
        self._columns = []
        self.csvr = csv.reader(self.fileobj, dialect=self.dialect)

    def __iter__(self):
        return self.rows
            
    @property
    def rows(self):
        ''' Iterator for rows, caching into row list '''
        if self._rows:
            return iter(self._rows)
        else:
            return self._row_iterator()

    @property
    def columns(self):
        if not self._columns:
            if self.cols_first:
                self.fileobj.seek(0)
                self._columns = self.csvr.next()
        return self._columns

    def _row_iterator(self):
        ''' Iterate over file returning rows, cache result if complete '''
        self.fileobj.seek(0)
        if self.cols_first:
            self._columns = self.csvr.next()
        rows = []
        for row in self.csvr:
            res = self._rowparse(row)
            rows.append(res)
            yield res
        self._rows = rows
        
    def _rowparse(self, row):
        outd = {}
        for i, val in enumerate(row):
            name, converter = self.importers[i]
            outd[name] = converter(val)
        return outd

