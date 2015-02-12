#!/usr/bin/env python

class Event(object):

    def __init__(self, type_, data=None):
        """ Initializes an event.

        Args:
            type_ (EventTypeEnum): The type of event this is.
            data (optional): can be any data that needs to be passed. Best
                practice should dictate that events that inherit from this
                base class should define more specific data member variables.
        """
        self.event_type = type_
        self.data = data
