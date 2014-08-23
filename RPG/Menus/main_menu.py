#!/usr/bin/env python

from RPG.Menus.menu import Menu, MenuOption, MatchTemplate
from RPG.event import Event
from RPG.event_dispatcher import EventTypeEnum

class MainMenu(Menu):

    def __init__(self):
        super(MainMenu, self).__init__()

        # Setup play option
        matches = [MatchTemplate('partial_string', '1'),
                   MatchTemplate('regex', r'[Pp]lay')]
        #TODO this should really be a MenuEvent once it is implemented
        menu_play_event = Event(EventTypeEnum.MENU_MAIN_PLAY)
        play_option = MenuOption('1) Play', matches, menu_play_event)
        self.add_option(play_option)

    def as_string(self, size):
        #TODO need to center the text using size
        string = " ____  ____   ____\n"
        string+= "|  _ \|  _ \ / ___|\n"
        string+= "| |_) | |_) | |  _\n"
        string+= "|  _ <|  __/| |_| |\n"
        string+= "|_| \_\_|    \____|\n"
        string+= "-------------------\n"
        for option in self.options:
            string += option.msg + "\n"
        return string
