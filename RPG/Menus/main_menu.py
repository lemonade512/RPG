#!/usr/bin/env python

from RPG.Menus.menu import Menu, MenuOption, MatchTemplate
from RPG.event import Event
from RPG.event_dispatcher import EventTypeEnum

class MainMenu(Menu):

    def __init__(self):
        super(MainMenu, self).__init__()

        # Setup new option
        matches = [MatchTemplate('regex', r'[Nn]ew')]
        #TODO this should really be a MenuEvent once it is implemented
        menu_new_event = Event(EventTypeEnum.MENU_MAIN_NEW)
        new_option = MenuOption('New', matches, menu_new_event)
        self.add_option(new_option)

        # Setup load option
        matches = [MatchTemplate('regex', r'[Ll]oad')]
        menu_load_event = Event(EventTypeEnum.MENU_MAIN_LOAD)
        load_option = MenuOption('Load', matches, menu_load_event)
        self.add_option(load_option)

        # Setup help option
        matches = [MatchTemplate('regex', r'[Hh]elp')]
        menu_help_event = Event(EventTypeEnum.MENU_MAIN_HELP)
        help_option = MenuOption('Help', matches, menu_help_event)
        self.add_option(help_option)

    def as_string(self, size):
        #TODO need to center the text using size
        x_size = size[1]
        halfway = x_size / 2
        str_len = len(" ____  ____   ____")
        left_pad = halfway - (str_len/2)
        string = left_pad*' ' + " ____  ____   ____ \n"
        string+= left_pad*' ' + "|  _ \|  _ \ / ___|\n"
        string+= left_pad*' ' + "| |_) | |_) | |  _ \n"
        string+= left_pad*' ' + "|  _ <|  __/| |_| |\n"
        string+= left_pad*' ' + "|_| \_\_|    \____|\n"
        string+= left_pad*' ' + "-------------------\n"
        string+=super(MainMenu, self).as_string(size)
        return string
