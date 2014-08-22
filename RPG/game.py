#!/usr/bin/env python
'''
This class keeps track of the player and the event queue.
'''
import signal
from RPG.event_dispatcher import EventDispatcher
from RPG.time_keeper import TimeKeeper, Time
from RPG.iohandler import IOHandler
from RPG.Menus.main_menu import MainMenu

class Game:

    def __init__(self):
        self.player = None
        self.event_dispatcher = EventDispatcher()
        self.io_handler = IOHandler(self.event_dispatcher)
        self.time_keeper = TimeKeeper(self.event_dispatcher)
        self.time_keeper.current_time = Time(1000, 1, 1, 8, 0, 0)
        #self.battle_engine = BattleEngine(self.event_dispatcher)

        self.current_menu = MainMenu()

        self.playing = False

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

if __name__ == "__main__":
    game = Game()
    game.start()
