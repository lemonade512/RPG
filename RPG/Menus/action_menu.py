#!/usr/bin/env python

from RPG.Menus.menu import Menu, MenuOption, MatchTemplate
from RPG.event import Event
from RPG.event_dispatcher import EventTypeEnum

class ActionMenu(Menu):

    def __init__(self):
        super(ActionMenu, self).__init__()

        # Setup move option
        matches = [MatchTemplate('partial_string', '1'),
                   MatchTemplate('regex', r'[Mm]ove')]
        menu_move_event = Event(EventTypeEnum.MENU_ACTION_MOVE)
        move_option = MenuOption('1) Move', matches, menu_move_event)
        self.add_option(move_option)

    def as_string(self, size):
        string = "What would you like to do?\n"
        for option in self.options:
            string += option.msg + "\n"
        return string
