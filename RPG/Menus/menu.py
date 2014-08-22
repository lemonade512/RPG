#!/usr/bin/env python
'''
This class provides the basic functionality for menus.
'''

# Standard library imports
import os
import sys
import time
import re
from collections import namedtuple

# Project Imports
from RPG.event_dispatcher import EventDispatcher, EventTypeEnum

MatchTemplate = namedtuple('MatchTemplate', 'match_type match_string')
#TODO should MatchTemplate be a class with a match method? It could then be subclassed into
# other match objects like RegexMatchTemplate and FullStringMatchTemplate with overloaded
# match methods

class MenuOption:

    def __init__(self, msg, match_list, event):
        '''
        match_list is a list containing MatchTemplate's
                This allows using many different
        msg is the string representation of this option
        '''
        self.msg = msg
        self.match_list = match_list
        self.event = event

    def __eq__(self, other):
        if isinstance(other, str):
            return self.check_match(other)
        else:
            return NotImplemented

    def __str__(self):
        return self.msg

    def check_match(self, string):
        '''
        returns True if string matches MatchOption
        returns False if string does not match MatchOption
        '''
        for template in self.match_list:
            if template.match_type == 'regex':
                regex = re.compile(template.match_string)
                match = regex.match(string)
                if match:
                    return True
            elif template.match_type == 'full_string':
                if string == template.match_string:
                    return True
            elif template.match_type == 'partial_string':
                if template.match_string in string:
                    return True

        return False

class Menu(object):
    '''
    WARNING: When you are creating menus make sure that there isn't
    input that could match multiple options
    '''

    def __init__(self):
        self.options = []

    def add_option(self, menu_option):
        self.options.append(menu_option)

    def as_string(self, size):
        string = "Size: " + str(size) +"\n"
        string += "What would you like to do?\n"
        for option in self.options:
            string += repr(option.msg) + '\n'
        return string
