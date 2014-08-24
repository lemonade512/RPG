#!/usr/bin/env python
import sys
import StringIO
from RPG.Menus.menu import Menu, MenuOption, MatchTemplate, Page
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

    def test_page_has_space(self):
        page = Page(20, 3, 3, 0)
        opt = MenuOption('Option 1', [], None)
        assert_true(page.has_space(opt, False))
        assert_true(page.has_space(opt, True))

    def test_page_assert_error(self):
        page = Page(2, 3, 3, 0)
        opt = MenuOption('Option 1', [], None)
        assert_raises(AssertionError, page.has_space, opt, True)
        assert_raises(AssertionError, page.has_space, opt, False)

    def test_page_string_one_opt(self):
        page = Page(15, 1, 3, 0)
        opt = MenuOption('Option', [], None)
        page.add_options([opt])
        assert_equal(str(page), '1) Option      ')

    def test_page_string_two_opts(self):
        page = Page(10, 2, 3, 0)
        opt1 = MenuOption('Option 1 is long', [], None)
        opt2 = MenuOption('Option 2', [], None)
        page.add_options([opt1, opt2])
        string = '1) Option 1 is long \n'
        string+= '2) Option 2         '
        assert_equal(str(page), string)
