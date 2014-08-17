#!/usr/bin/env python
""" getTerminalSize()
 - get width and height of console
 - works on linux,os x,windows,cygwin(windows)
"""

import sys
import os
import tty, fcntl, termios

# Define behaviour of from utils import *
# will only import getTerminalSize
__all__=['getTerminalSize', 'UserInput']


class UserInput:
    def __init__(self):
        self.in_buf = ''
        self.code = None
        self.char = None
        self.in_escape = False
        self.in_ansi = False

        self.fd = sys.stdin.fileno()
        # save old state
        self.flags_save = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        self.attrs_save = termios.tcgetattr(self.fd)

    def onKeyPress(self, c):
        '''
        up key:
        down key:
        left key:
        right key:
        '''
        if c == '':
            return
        self.code = ord(c)

        if self.in_escape and self.code != 91 and not self.in_ansi:
            self.in_escape = False

        if self.in_ansi and self.code not in [65, 66, 67, 68]:
            print "Unhandled ansi sequence"
            self.in_escape = False
            self.in_ansi = False
            return

        if self.code == 27:
            # start of ESC sequence
            self.in_escape = True
            return

        if self.in_escape and self.code == 91:
            # start of Ansi sequence
            self.in_ansi = True
            return

        if self.in_ansi and self.code in [65,66,67,68]:
            # Arrow key ansi sequence
            self.in_escape = False
            self.in_ansi = False
            return

        if self.code == 3:
            raise(KeyboardInterrupt)
        self.char = c
        if self.code == 127:
            if len(self.in_buf) > 0:
                sys.stdout.write('\b \b')
                self.in_buf = self.in_buf[:-1]
            return
        self.in_buf += self.char
        sys.stdout.write(c)

    def get_input(self):
        '''
        enter = 13
        ctrl-c = 3
        '''
        while self.code != 13:
            self.onKeyPress(self.read_single_keypress())
        sys.stdout.write('\n')
        return self.in_buf

    def clear_input(self):
        self.code = None
        self.char = None
        self.in_buf = ''

    def read_single_keypress(self):
        """Waits for a single keypress on stdin.

        This is a silly function to call if you need to do it a lot because it has
        to store stdin's current setup, setup stdin for reading single keystrokes
        then read the single keystroke then revert stdin back after reading the
        keystroke.

        Returns the character of the key that was pressed (zero on
        KeyboardInterrupt which can happen when a signal gets handled)

        Gotten from http://stackoverflow.com/questions/983354/how-do-i-make-python-to-wait-for-a-pressed-key
        """
        import termios, fcntl, sys, os
        # make raw - the way to do this comes from the termios(3) man page.
        attrs = list(self.attrs_save) # copy the stored version to update
        # iflag
        attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK
                      | termios.ISTRIP | termios.INLCR | termios. IGNCR
                      | termios.ICRNL | termios.IXON )
        # oflag
        attrs[1] &= ~termios.OPOST
        # cflag
        attrs[2] &= ~(termios.CSIZE | termios. PARENB)
        attrs[2] |= termios.CS8
        # lflag
        attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
                      | termios.ISIG | termios.IEXTEN)
        termios.tcsetattr(self.fd, termios.TCSANOW, attrs)
        # turn off non-blocking
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.flags_save & ~os.O_NONBLOCK)
        # read a single keystroke
        try:
            ret = sys.stdin.read(1) # returns a single character
        except KeyboardInterrupt:
            ret = 0
        except IOError:
            ret = ''
        finally:
            # restore old state
            self.restore_term()
        return ret

    def restore_term(self):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.attrs_save)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.flags_save)

def getTerminalSize():
   import platform
   current_os = platform.system()
   tuple_xy=None
   if current_os == 'Windows':
       tuple_xy = _getTerminalSize_windows()
       if tuple_xy is None:
          tuple_xy = _getTerminalSize_tput()
          # needed for window's python in cygwin's xterm!
   if current_os == 'Linux' or current_os == 'Darwin' or  current_os.startswith('CYGWIN'):
       tuple_xy = _getTerminalSize_linux()
   if tuple_xy is None:
       print "default"
       tuple_xy = (80, 25)      # default value
   return tuple_xy

def _getTerminalSize_windows():
    res=None
    try:
        from ctypes import windll, create_string_buffer

        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12

        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
    except:
        return None
    if res:
        import struct
        (bufx, bufy, curx, cury, wattr,
         left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
        sizex = right - left + 1
        sizey = bottom - top + 1
        return sizex, sizey
    else:
        return None

def _getTerminalSize_tput():
    # get terminal width
    # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    try:
       import subprocess
       proc=subprocess.Popen(["tput", "cols"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
       output=proc.communicate(input=None)
       cols=int(output[0])
       proc=subprocess.Popen(["tput", "lines"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
       output=proc.communicate(input=None)
       rows=int(output[0])
       return (cols,rows)
    except:
       return None


def _getTerminalSize_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,'1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])

if __name__ == "__main__":
    sizex,sizey=getTerminalSize()
    print  'width =',sizex,'height =',sizey
