#!/usr/bin/env python
from RPG.event_dispatcher import EventDispatcher, EventTypeEnum
from RPG.event import Event

class TestEventDispatcher():

    @classmethod
    def setup_class(cls):
        cls.dispatcher = EventDispatcher()

    def setup(self):
        self.received_event = False

    def teardown(self):
        self.received_event = False
        self.dispatcher.clear_handlers()

    def callback(self, event):
        self.received_event = True

    def test_add_handler(self):
        self.dispatcher.add_handler(EventTypeEnum.GAME_START,
                            self.callback)
        event = Event(EventTypeEnum.GAME_START)
        self.dispatcher.dispatch(event)
        assert(self.received_event)

    def test_remove_handler(self):
        self.dispatcher.add_handler(EventTypeEnum.GAME_QUIT,
                            self.callback)
        event = Event(EventTypeEnum.GAME_QUIT)
        self.dispatcher.dispatch(event)
        assert(self.received_event)
        self.received_event = False
        self.dispatcher.remove_handler(EventTypeEnum.GAME_QUIT,
                               self.callback)
        self.dispatcher.dispatch(event)
        print self.dispatcher.event_handlers
        assert(not self.received_event)
