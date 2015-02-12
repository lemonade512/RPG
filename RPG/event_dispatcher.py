#!/usr/bin/env python

""" This class allows objects to register for different event messages.
The dispather will receive all events and send them out to their
proper recipients.
"""


class EventTypeEnum(object):
    """ Available events. """
    GAME_START='game started'
    GAME_QUIT='game quit'

    MENU_MAIN_NEW='main menu new'
    MENU_MAIN_LOAD='main menu load'
    MENU_MAIN_HELP='main menu help'
    MENU_ACTION_MOVE='action menu move'
    MENU_NEXT_PAGE='menu next page'
    MENU_PREVOUS_PAGE='menu previous page'

    # NOTE this is here to satisfy pylint
    def __init__(self):
        pass

class EventDispatcher(object):
    """ An object to dispatch events to registered observers.

    Attributes:
        event_handlers (dict): Dictionary that holds a list of callbacks for
            every event. The keys of the dictionary are the strings representing
            the possible events.
    """

    def __init__(self):
        self.event_handlers = dict()

    def add_handler(self, event_type, handler):
        """ Add a callback for the given event type.

        Args:
            event_type (EventTypeEnum): The event to listen to.
            handler: The function to call on the occurence of the event. The
                handler must take a single argument of the event.
        """
        if event_type in self.event_handlers:
            self.event_handlers[event_type].append(handler)
        else:
            self.event_handlers[event_type] = [handler]

    def remove_handler(self, event_type, handler):
        """ Removes the given handler from the dictionary.

        Args:
            event_type (EventTypeEnum): The event that the handler is observing.
            handler: The function that is handling the event.
        """
        for h in self.event_handlers[event_type]:
            if handler == h:
                self.event_handlers[event_type].remove(h)

    def clear_handlers(self):
        """ Removes all the callback functions from the dictionary. """
        self.event_handlers = dict()

    def dispatch(self, event):
        """ Calls the callback functions for the given event.

        Args:
            event (Event): The event we are dispatching. If this is None
                the function does nothing.
        """
        if event == None:
            return

        if event.event_type not in self.event_handlers:
            return

        for handler in self.event_handlers[event.event_type]:
            handler(event)
