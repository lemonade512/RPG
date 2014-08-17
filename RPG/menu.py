#!/usr/bin/env python
'''
This class provides the basic functionality for menus.
'''
import os
import sys
import time
import re
import signal
#from RPG.event_dispatcher import EventDispatcher, EventTypeEnum

# This line should be changed to above when you work out pathing issues
from event_dispatcher import EventDispatcher, EventTypeEnum
from utils import getTerminalSize, UserInput
from collections import namedtuple

MatchTemplate = namedtuple('MatchTemplate', 'match_type match_string')
#TODO should MatchTemplate be a class with a match method? It could then be subclassed into
# other match objects like RegexMatchTemplate and FullStringMatchTemplate with overloaded
# match methods

class MenuOption:

    def __init__(self, msg, match_list, event):
        '''
        match_list is a list containing MatchTemplate's
                This allows using many different
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

class Menu:
    '''
    WARNING: When you are creating menus make sure that there isn't
    input that could match multiple options
    '''

    def __init__(self):
        self.options = []

    def add_option(self, menu_option):
        self.options.append(menu_option)

# SHOULD BE HANDLED BY INPUT_MANAGER
#    def get_input(self):
#        while True:
#            user_in = self.user_input.get_input()
#            self.user_input.clear_input()
#            #user_in = raw_input()
#            print "User input: " + str(user_in)
#            # check what menu option matches user input
#            for opt in self.options:
#                if opt == user_in:
#                    print "Matched: " + str(opt)
#                    self.dispatcher.dispatch(opt.event)
#                    return
#
#            print "INVALID INPUT"
#            print ">>> ",


if __name__ == "__main__":
    menu = Menu([])
    mt = MatchTemplate('regex', r'hell')
    menu.add_option(MenuOption('option 1', [mt], None))
    mt = MatchTemplate('full_string', '2')
    menu.add_option(MenuOption('option 2', [mt], None))
    menu.show()
    menu.get_input()
