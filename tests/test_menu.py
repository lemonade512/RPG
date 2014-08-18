#!/usr/bin/env python
import sys
import StringIO
from RPG.menu import Menu, MenuOption, MatchTemplate
from RPG.event_dispatcher import EventDispatcher, EventTypeEnum
from RPG.event import Event
from nose.tools import *

class TestMenu():

    def test_menu_option_match_full_string(self):
        mt = MatchTemplate('full_string', 'opt1')
        menu_option = MenuOption('opt1', [mt], None)
        assert_true(menu_option == 'opt1')
        assert_false(menu_option == 'opt')
        assert_false(menu_option == 'opt12')

    def test_menu_option_match_partial_string(self):
        mt = MatchTemplate('partial_string', 'opt1')
        menu_option = MenuOption('opt1', [mt], None)
        assert_true(menu_option == 'opt1')
        assert_false(menu_option == 'opt')
        assert_true(menu_option == 'opt1234')

    def test_menu_option_match_regex(self):
        mt = MatchTemplate('regex', r'o.*1')
        menu_option = MenuOption('opt1', [mt], None)
        assert_true(menu_option == 'opt1')
        assert_false(menu_option == 'opt')
        assert_true(menu_option == 'option1')
        assert_false(menu_option == 'hoption1lp')
        assert_true(menu_option == 'option1lpe')
