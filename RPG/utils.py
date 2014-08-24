#!/usr/bin/env python

def lookahead(iterable):
    ''' Gotten from http://stackoverflow.com/questions/1630320/what-is-the-pythonic-way-to-detect-the-last-element-in-a-python-for-loop
    Returns val, True on the last element
    '''
    it = iter(iterable)
    last = it.next()
    for val in it:
        yield last, False
        last = val
    yield last, True
