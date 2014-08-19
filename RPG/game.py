#!/usr/bin/env python
'''
This class keeps track of the player and the event queue.
'''

class Game:

    def __init__(self):
        self.player = None
        self.event_dispatcher = EventDispatcher()
        self.io_handler = IOHandler(self.event_dispatcher)
        self.time_keeper = TimeKeeper(self.event_dispatcher)
        self.time_keeper.current_time = Time(1000, 1, 1, 8, 0, 0)
        #self.battle_engine = BattleEngine(self.event_dispatcher)

        self.current_menu = ActionMenu()

        self.playing = False

        signal.signal(signal.SIGWINCH, self.window_changed)

    def main(self):
        with self.io_handler:
            #self.load()
            self.start()
            #self.quit()

    def start(self):
        # If no player go through player creation

        # Main game loop
        self.playing = True
        while self.playing:
            menu = self.current_menu
            self.io_handler.show_menu(menu)
            self.io_handler.get_input()

    def window_changed(self, *args):
        self.io_handler.refresh_screen()
