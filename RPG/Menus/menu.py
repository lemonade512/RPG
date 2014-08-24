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
from RPG.event import Event
from RPG.utils import lookahead

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

        # TODO IS there a better way?
        self.number_match = None # used for number on page
        self.number_string = ''

    def __eq__(self, other):
        if isinstance(other, str):
            return self.check_match(other)
        else:
            return NotImplemented

    def __str__(self):
        return self.number_string + self.msg

    def __repr__(self):
        return self.__str__()

    def check_match(self, string):
        '''
        returns True if string matches MatchOption
        returns False if string does not match MatchOption
        '''
        m_list = self.match_list
        if self.number_match != None:
            m_list.append(self.number_match)

        for template in m_list:
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

class Page(object):

    def __init__(self, col_size, num_rows, num_cols, pad):
        self.col_size = col_size
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.options = []
        self.next_page = None
        self.prev_page = None

        self.pad = pad

        # (curr_row, curr_col) is the next empty spot
        self.curr_col = 0
        self.curr_row = 0

    def __str__(self):
        string = ""
        curr_col = 0
        curr_row = 0
        for opt in self.options:
            cols_left  = self.num_cols - curr_col
            span = (len(str(opt)) / self.col_size) + 1
            if span > cols_left:
                curr_row += 1
                curr_col = span
                if span > 1 and cols_left != 0:
                    string += '\n'
                else:
                    string += ' '*self.pad
                #string += ' '*self.pad
                fmt = '{:+<'+str(self.col_size*span)+'}'
                #fmt = '{:<'+str(self.col_size*span)+'}'
                string += fmt.format(str(opt))
            else:
                curr_col += span
                fmt = '{:=<'+str(self.col_size*span)+'}'
                #fmt = '{:<'+str(self.col_size*span)+'}'
                string += fmt.format(str(opt))
        return string

    def match(self, user_in):
        for opt in self.options:
            if opt == user_in:
                return opt
        return None

    def has_space(self, opt, is_last):
        '''
        is_last: a boolean telling whether this is the last option
                 to add or if there are more options
        '''
        span = (len(str(opt)) / self.col_size) + 1
        assert(span < self.num_cols)
        last_row = self.num_rows - 1
        cols_left  = self.num_cols - self.curr_col

        # On last row, more options left, not enough room for
        # next page option
        if (self.curr_row == last_row and
                not is_last and
                span == cols_left):
            return False

        # On last row, span greater than cols left
        if self.curr_row == last_row and span > cols_left:
            return False

        if (self.curr_row != last_row and
                span == self.num_cols and
                not is_last):
            return False

        return True

    def add_options(self, options):
        # NOTE this function can only be called once
        opt_num = 1
        for opt, last in lookahead(options):
            opt.number_string = str(opt_num) + ') '
            if self.has_space(opt, last):
                opt.number_match = MatchTemplate('full_string', str(opt_num))
                opt_num += 1
                span = (len(str(opt)) / self.col_size) + 1
                self.options.append(opt)
                if self.curr_col + span > self.num_cols:
                    self.curr_row += 1
                    self.curr_col = span
                elif self.curr_col + span == self.num_cols:
                    self.curr_row += 1
                    self.curr_col = 0
                else:
                    self.curr_col += span
            else:
                # Create prev_page_option and next_page
                self.next_page = Page(self.col_size, self.num_rows, self.num_cols, self.pad)
                self.next_page.prev_page = self
                matches = [MatchTemplate('regex', r'[Pp]rev')]
                menu_prev_page_event = Event(EventTypeEnum.MENU_PREVOUS_PAGE)
                prev_page_option = MenuOption('Previous Page', matches, menu_prev_page_event)
                next_page_opts = [prev_page_option]
                next_page_opts += options[opt_num-1:]
                self.next_page.add_options(next_page_opts)

                # create and add next_page_option
                matches = [MatchTemplate('regex', r'[Nn]ext')]
                menu_next_page_event = Event(EventTypeEnum.MENU_NEXT_PAGE)
                next_page_option = MenuOption('Next Page', matches, menu_next_page_event)
                next_page_option.number_string = str(opt_num) + ') '
                next_page_option.number_match = MatchTemplate('full_string', str(opt_num))

                self.options = self.options[:opt_num-1]
                self.options.append(next_page_option)
                return

class Menu(object):
    '''
    WARNING: When you are creating menus make sure that there isn't
    input that could match multiple options
    '''
    COL_SIZE = 20
    MAX_ROWS = 3

    def __init__(self):
        self.options = []
        self.prev_size = None
        self.curr_page = None
        self.page_num = 0

    def add_option(self, menu_option):
        self.options.append(menu_option)

    def next_page(self):
        self.page_num += 1
        self.curr_page = self.curr_page.next_page

    def prev_page(self):
        self.page_num -= 1
        self.curr_page = self.curr_page.prev_page

    def match(self, user_in):
        '''
        Returns the option that matches user_in or None if no
        option exists
        '''
        opt = self.curr_page.match(user_in)
        return opt

    def create_pages(self, size):
        ''' This should be called anytime the console size changes '''
        num_cols = size[1] / Menu.COL_SIZE
        col_size = size[1] / num_cols

        # Sometimes there is a small pad of extra space at the end
        pad = size[1] - (num_cols * col_size)

        self.curr_page = Page(col_size, Menu.MAX_ROWS, num_cols, pad)
        self.curr_page.add_options(self.options)

    def as_string(self, size):
        if self.prev_size != size:
            self.create_pages(size)
            self.prev_size = size
            page_num = 0
            while (self.curr_page.next_page != None and
                   page_num != self.page_num):
                self.curr_page = self.curr_page.next_page
                page_num += 1
            self.page_num = page_num

        string = "Menu\n"
        string+= str(self.curr_page)
        return string
