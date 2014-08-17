#!/usr/bin/env python
'''
This class allows objects to register for different event messages.
The dispather will receive all events and send them out to their
proper recipients.
'''

class EventTypeEnum:
    GAME_START='game started'
    GAME_QUIT='game quit'

    MENU_TEST='test menu events'

class EventDispatcher:

    def __init__(self):
        self.event_handlers=dict()

    def add_handler(self, event_type, handler):
        '''
        event_type is taken from the EventTypeEnum defined above
        handler is a function that will be called when an event of event_type is dispatched
        '''
        if event_type in self.event_handlers:
            self.event_handlers[event_type].append(handler)
        else:
            self.event_handlers[event_type] = [handler]

    def remove_handler(self, event_type, handler):
        for h in self.event_handlers[event_type]:
            if handler == h:
                self.event_handlers[event_type].remove(h)

    def clear_handlers(self):
        self.event_handlers = dict()

    def dispatch(self, event):
        if event.event_type not in self.event_handlers:
            return

        for handler in self.event_handlers[event.event_type]:
            handler(event)
