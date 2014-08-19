#!/usr/bin/env python
'''
This class handles all output to the screen and input from the user.

Author: Phillip Lemons
Date: 8/16/14
'''

import sys
import os
import time
import curses

class IOHandler:

    def __init__(self, event_dispatcher):
        self.in_buf = ''
        self.output_log_name = 'output_log.txt'

        self.input_pos = None
        self.after_menu_pos = None

        self.dispatcher = event_dispatcher
        self.current_menu = None

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
        if os.path.isfile(self.output_log_name):
            os.remove(self.output_log_name)

    @property
    def screen_size(self):
        return self.stdscr.getmaxyx()

    def show_menu(self, menu):
        # TODO handle error that happens when window gets too small
        # TODO will need to create columns for options
        self.current_menu = menu
        self.clear_screen()
        self.stdscr.addstr(self.current_menu.as_string(self.screen_size))
        self.stdscr.addstr('-'*self.screen_size[1])
        self.stdscr.refresh()
        self.after_menu_pos = self.stdscr.getyx()
        # print output from output_log

    def refresh(self):
        self.clear_screen()
        self.show_menu(self.current_menu)
        self.input_pos = None
        self.write_to_input('>>> ' + self.in_buf)

        top_left = self.after_menu_pos
        max_pos = self.stdscr.getmaxyx()
        bottom_right = (max_pos[0]-2, max_pos[1]-1)
        lines = bottom_right[0] - top_left[0]
        prev_output = self.tail_output(lines)
        self.write_to_log(prev_output, write_to_file=False)

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

    def tail_output(self, window=20):
        '''
        Gotten from stack overflow
        '''
        with open(self.output_log_name, 'r') as f:
            BUFSIZ = 1024
            f.seek(0, 2)
            bytes = f.tell()
            size = window
            block = -1
            data = []
            while size > 0 and bytes > 0:
                if (bytes - BUFSIZ > 0):
                    # Seek back one whole BUFSIZ
                    f.seek(block*BUFSIZ, 2)
                    # read BUFFER
                    data.append(f.read(BUFSIZ))
                else:
                    # file too small, start from begining
                    f.seek(0,0)
                    # only read what was not read
                    data.append(f.read(bytes))
                linesFound = data[-1].count('\n')
                size -= linesFound
                bytes -= BUFSIZ
                block -= 1
            return '\n'.join(''.join(data).splitlines()[-window:])

    def num_lines(self, string):
        term_size = self.stdscr.getmaxyx()
        num_lines = (len(string) / term_size[1]) + 1
        num_lines += string.count('\n')
        return num_lines

    def write_to_log(self, string='', write_to_file=True):
        '''
        writes string to the main log section of the window
        '''
        top_left = self.after_menu_pos
        max_pos = self.stdscr.getmaxyx()
        bottom_right = (max_pos[0]-2, max_pos[1]-1)
        if bottom_right[0] < top_left[0]:
            return

        self.stdscr.setscrreg(top_left[0], bottom_right[0])
        self.stdscr.scrollok(1)
        lines = self.num_lines(string)
        self.stdscr.scroll(lines)
        self.stdscr.scrollok(0)

        self.stdscr.move(bottom_right[0]-lines+1, 0)
        self.stdscr.addstr(string)

        if write_to_file:
            output_log = open(self.output_log_name, 'a')
            output_log.write(string+'\n')
            output_log.flush()
            output_log.close()

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
                    self.dispatcher.dispatch(opt.event)
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

    from event_dispatcher import EventDispatcher
    dispatcher = EventDispatcher()
    io_handler = IOHandler(dispatcher)

    with io_handler:
        io_handler.show_menu(m)
        while True:
            inp = io_handler.get_input()
