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
import locale

locale.setlocale(locale.LC_ALL, "")

class IOHandler:

    def __init__(self, event_dispatcher):
        self.in_buf = ''
        self.output_log_name = 'output_log.txt'

        self.input_pos = None

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
    def num_log_lines(self):
        top_left = self.after_menu_pos
        max_pos = self.stdscr.getmaxyx()
        bottom_right = (max_pos[0]-2, max_pos[1]-1)
        lines = bottom_right[0] - top_left[0]
        return lines

    def show_menu(self, menu):
        # TODO will need to create columns for options
        self.current_menu = menu
        self.stdscr.erase()
        max_y, max_x = self.stdscr.getmaxyx()

        # Setup Menu window
        menu_string = self.current_menu.as_string((max_y, max_x))
        menu_size = self.num_lines(menu_string)
        self.menu_border_win = self.stdscr.derwin(menu_size+1, max_x, 0,0)
        self.menu_win = self.menu_border_win.derwin(menu_size, max_x-2, 1,1)
        self.menu_win.addstr(menu_string)
        self.menu_border_win.border()

        # Setup Log window
        #NOTE assumes input window size of 3 lines
        # subtract extra 1 for log border
        log_size = max_y - (menu_size+1) - 3 - 1
        self.log_border_win = self.stdscr.derwin(log_size+1, max_x, menu_size+1, 0)
        self.log_win = self.log_border_win.derwin(log_size, max_x-2, 1, 1)
        self.log_border_win.border()

        # Setup Input window
        self.input_border_win = self.stdscr.derwin(3, max_x, menu_size+log_size + 2, 0)
        self.input_win = self.input_border_win.derwin(1, max_x-2, 1, 1)
        self.input_border_win.border()

        self.stdscr.refresh()
        # print output from output_log
        #prev_output = self.tail_output(self.num_log_lines)
        #self.write_to_log(prev_output, write_to_file=False)

    def refresh(self):
        self.clear_screen()
        self.show_menu(self.current_menu)
        self.input_pos = None
        self.write_to_input('>>> ' + self.in_buf)

        prev_output = ''.join(self.tail_output(self.num_log_lines+10))
        self.write_to_log(prev_output, write_to_file=False)

    def on_backspace(self):
        # make sure not to delete prompt
        if len(self.in_buf) == 0:
            return

        # delete the previously input character
        pos = self.input_win.getyx()
        self.input_win.move(pos[0], pos[1]-1)
        self.input_win.delch()
        self.input_pos = self.input_win.getyx()
        self.input_win.refresh()

    def write_to_input(self, string):
        '''
        writes to the input section of self.stdscr
        '''
        max_x = self.input_win.getmaxyx()[1]
        cur_x = self.input_win.getyx()[1]
        if cur_x + len(string) >= max_x:
            return False
        if self.input_pos == None:
            self.input_pos = (0,0)
        self.input_win.move(*self.input_pos)
        self.input_win.addstr(string)
        self.input_pos = self.input_win.getyx()
        self.input_win.refresh()
        return True

    def tail_output(self, window=20):
        '''
        Gotten from stack overflow
        '''
        if not os.path.isfile(self.output_log_name):
            return

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
        if string == None:
            return 0
        lines = string.split('\n')
        term_size = self.stdscr.getmaxyx()
        num_lines = 0
        for line in lines:
            num_lines+= (len(line) / term_size[1]) + 1
        return num_lines

    def write_to_log(self, string='', write_to_file=True):
        '''
        writes string to the main log section of the window
        '''
        max_y, max_x = self.log_win.getmaxyx()

        self.log_win.scrollok(1)
        lines = self.num_lines(string)
        self.log_win.setscrreg(0, max_y-2)
        self.log_win.scroll(lines)
        self.log_win.scrollok(0)

        # Fix bug where lines > num lines in window
        self.log_win.move(max_y-lines-1, 0)
        self.log_win.addstr(string)
        #self.stdscr.addstr(top_left[0], top_left[1], u'\u2588'.encode('utf-8'))

        if write_to_file:
            output_log = open(self.output_log_name, 'a')
            output_log.write('\n'+string)
            output_log.flush()
            output_log.close()

        self.log_win.refresh()

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
        self.input_win.erase()

        # allow the next call to write_to_input to reset input_pos
        self.input_pos = None
        return inp

    def get_input(self):
        menu = self.current_menu
        user_in = ''
        while True:
            self.write_to_input('>>> ')
            user_in = self.raw_input().strip()
            self.write_to_log('User input: ' + user_in)
            for opt in self.current_menu.options:
                if opt == user_in:
                    self.write_to_log("Matched: " + str(opt) + '\n')
                    self.dispatcher.dispatch(opt.event)
                    return

            self.write_to_log("INVALID INPUT\n")

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
