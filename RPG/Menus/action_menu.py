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
        move_option = MenuOption('Move', matches, menu_move_event)
        self.add_option(move_option)

        # Setup test options
        opt1 = MenuOption('Kill', [], None)
        self.add_option(opt1)
        opt2 = MenuOption('Run', [], None)
        self.add_option(opt2)
        opt3 = MenuOption('Kick', [], None)
        self.add_option(opt3)
        opt4 = MenuOption('Hunt', [], None)
        self.add_option(opt4)
        opt5 = MenuOption('Fight', [], None)
        self.add_option(opt5)
        opt6 = MenuOption('This is a really long option', [], None)
        self.add_option(opt6)
        opt7 = MenuOption('Option', [], None)
        self.add_option(opt7)
        opt8 = MenuOption('Party', [], None)
        self.add_option(opt8)

    def as_string(self, size):
        string = "What would you like to do?\n"
        string += super(ActionMenu, self).as_string(size)
        return string
