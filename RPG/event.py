#!/usr/bin/env python

class Event:

    def __init__(self, _type, data=None):
        '''
        _type should be taken from EventTypeEnum in event_dispatcher
        data can be any data that needs to be passed. Best practice should dictate
        that events that inherit from this base class should define more specific
        data member variables.
        '''
        self.event_type = _type
        self.data = data
