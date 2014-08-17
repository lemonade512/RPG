#!/usr/bin/env python
'''
This class handles all output to the screen and input from the user.

Author: Phillip Lemons
Date: 8/16/14
'''

import sys
import os
import tty, fcntl, termios
import time
import curses

class IOHandler:

    def __init__(self, event_dispatcher, current_menu):
        self.in_buf = ''

        self.input_pos = None
        self.after_menu_pos = None

        self.dispatcher = event_dispatcher
        self.current_menu = current_menu
        # self.output_log = open('my_cool_file', 'rw')

    def __enter__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.raw()
        self.stdscr.keypad(1)

    def __exit__(self, type, value, traceback):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    @property
    def screen_size(self):
        return self.stdscr.getmaxyx()

    def show_menu(self, menu):
        self.current_menu = menu
        self.clear_screen()
        self.stdscr.addstr("What would you like to do?\n")
        for option in menu.options:
            self.stdscr.addstr(repr(option.msg)+'\n')
        self.stdscr.addstr('-'*self.screen_size[1])
        self.stdscr.refresh()
        self.after_menu_pos = self.stdscr.getyx()
        # print output from output_log

    def refresh(self):
        #TODO refresh the main log so that strings that
        # were two lines can be joined to one line (use
        # main output log file)
        self.clear_screen()
        self.show_menu(self.current_menu)
        self.input_pos = None
        self.write_to_input('>>> ' + self.in_buf)

    def on_backspace(self):
        # make sure not to delete prompt
        if len(self.in_buf) == 0:
            return

        # delete the previously input character
        pos = self.stdscr.getyx()
        self.stdscr.move(pos[0], pos[1]-1)
        self.stdscr.delch()
        self.input_pos = self.stdscr.getyx()

    def write_to_input(self, string):
        '''
        writes to the input section of self.stdscr
        '''
        max_x = self.stdscr.getmaxyx()[1]
        cur_x = self.stdscr.getyx()[1]
        if cur_x + len(string) >= max_x:
            return False
        if self.input_pos == None:
            pos = self.stdscr.getmaxyx()
            self.input_pos = (pos[0]-1, 0)
        self.stdscr.move(*self.input_pos)
        self.stdscr.addstr(string)
        self.input_pos = self.stdscr.getyx()
        return True

    def num_lines(self, string):
        term_size = self.stdscr.getmaxyx()
        num_lines = (len(string) / term_size[1]) + 1
        num_lines += string.count('\n')
        return num_lines

    def write_to_log(self, string=''):
        '''
        writes string to the main log section of the window
        '''
        top_left = self.after_menu_pos
        max_pos = self.stdscr.getmaxyx()
        bottom_right = (max_pos[0]-2, max_pos[1])

        self.stdscr.setscrreg(top_left[0], bottom_right[0])
        io_handler.stdscr.scrollok(1)
        lines = self.num_lines(string)
        self.stdscr.scroll(lines)
        io_handler.stdscr.scrollok(0)

        self.stdscr.move(bottom_right[0]-lines+1, 0)
        self.stdscr.addstr(string)

    def raw_input(self):
        '''
        Gets input from user until user presses Return
        Keeps the input in input_buf
        '''
        last_key = None
        while last_key != '\n':
            last_key = self.stdscr.getkey()
            if last_key == 'KEY_RESIZE':
                self.refresh()
                continue
            if last_key == 'KEY_BACKSPACE':
                self.on_backspace()
                self.in_buf = self.in_buf[:-1]
                continue
            if last_key in ['KEY_UP', 'KEY_DOWN',
                                 'KEY_LEFT', 'KEY_RIGHT']:
                continue
            if last_key == '':
                exit()

            if last_key != '\n':
                success = self.write_to_input(last_key)
                if success:
                    self.in_buf += last_key
        inp = self.in_buf
        self.in_buf = ''
        self.stdscr.deleteln()

        # allow the next call to write_to_input to reset input_pos
        self.input_pos = None
        return inp

    def get_input(self):
        menu = self.current_menu
        user_in = ''
        while True:
            self.write_to_input('>>> ')
            user_in = self.raw_input()
            self.write_to_log('User input: ' + user_in)
            for opt in self.current_menu.options:
                if opt == user_in:
                    self.write_to_log("Matched: " + str(opt) + '\n')
                    #self.dispatcher.dispatch(opt.event)
                    return

            self.write_to_log("INVALID INPUT\n")

    def clear_screen(self):
        self.stdscr.erase()

if __name__ == "__main__":
    from menu import Menu, MenuOption, MatchTemplate
    m = Menu()
    mt = MatchTemplate('partial_string', 'opt1')
    m.add_option(MenuOption('opt1', [mt], None))
    mt = MatchTemplate('partial_string', 'opt2')
    m.add_option(MenuOption('opt2', [mt], None))

    io_handler = IOHandler(None, m)
    with io_handler:
        io_handler.show_menu(m)
        while True:
            inp = io_handler.get_input()
