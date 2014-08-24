#!/usr/bin/env python
'''
This class keeps track of the player and the event queue.
'''
import signal
from RPG.event_dispatcher import EventDispatcher, EventTypeEnum
from RPG.time_keeper import TimeKeeper, Time
from RPG.iohandler import IOHandler
from RPG.Menus.main_menu import MainMenu
from RPG.Menus.action_menu import ActionMenu

class Game:

    def __init__(self):
        self.player = None
        self.event_dispatcher = EventDispatcher()
        self.io_handler = IOHandler(self.event_dispatcher)
        self.time_keeper = TimeKeeper(self.event_dispatcher)
        self.time_keeper.current_time = Time(1000, 1, 1, 8, 0, 0)
        #self.battle_engine = BattleEngine(self.event_dispatcher)

        self.register_for_events()

        self.current_menu = MainMenu()

        self.playing = False

    def register_for_events(self):
        self.event_dispatcher.add_handler(
                EventTypeEnum.MENU_MAIN_PLAY,
                self.handle_main_menu_play)
        self.event_dispatcher.add_handler(
                EventTypeEnum.MENU_ACTION_MOVE,
                self.handle_action_menu_move)
        self.event_dispatcher.add_handler(
                EventTypeEnum.MENU_NEXT_PAGE,
                self.handle_next_page)
        self.event_dispatcher.add_handler(
                EventTypeEnum.MENU_PREVOUS_PAGE,
                self.handle_previous_page)

    def main(self):
        with self.io_handler:
            #self.load()
            self.start()
            #self.quit()

    def start(self):
        # If no player go through player creation

        # Main game loop
        self.playing = True
        with self.io_handler:
            while self.playing:
                menu = self.current_menu
                self.io_handler.show_menu(menu)
                self.io_handler.get_input()

    def handle_main_menu_play(self, event):
        self.current_menu = ActionMenu()

    def handle_action_menu_move(self, event):
        self.current_menu = MainMenu()

    def handle_next_page(self, event):
        self.current_menu.next_page()

    def handle_previous_page(self, event):
        self.current_menu.prev_page()

if __name__ == "__main__":
    game = Game()
    game.start()
