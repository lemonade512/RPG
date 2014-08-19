#!/usr/bin/env python
'''
This class is meant to keep track of the current time in the world.
Any event that takes time should be registered for here. This class
will also handle any events that should take place in the future.
'''
from math import copysign

class TimeDelta:

    def __init__(self, year=0, month=0, day=0, hour=0, minute=0, second=0):
        self.years = year
        self.months = month
        self.days = day
        self.hours = hour
        self.minutes = minute
        self.seconds = second
        self.__repr__ = self.__str__

    def __str__(self):
        string = "Years: " + str(self.years) + " "
        string += "Months: " + str(self.months) + " "
        string += "Days: " + str(self.days) + " "
        string += "Hours: " + str(self.hours) + " "
        string += "Minutes: " + str(self.minutes) + " "
        string += "Seconds: " + str(self.seconds)
        return string

    def __eq__(self, other):
        if isinstance(other, TimeDelta):
            if (self.years == other.years and
                    self.months == other.months and
                    self.days == other.days and
                    self.hours == other.hours and
                    self.minutes == other.minutes and
                    self.seconds == other.seconds):
                return True
            else:
                return False
        else:
            return NotImplemented

class Time:
    '''
    1 year = 12 months
    1 month = 30 days
    1 day = 24 hours
    1 hour = 60 minutes
    1 minute = 60 seconds

    1 battle turn = 6 seconds
    1 local turn = 10 minutes
    1 week = 7 days

    Battle turns are used during battle or other fast-paced events.
    Local turns might be used when conversing with NPC's or waiting
    for a quest event.
    Days may be used when traveling long distances.
    '''

    def __init__(self, year, month, day, hour=0,
                 minute=0, second=0):
        '''
        NOTE: month is a num between 1 and 12 but is stored as a number
        between 0 and 11
        '''
        self.year = year
        assert(month <= 12 and month > 0)
        self.month = month-1
        assert(day <= 30 and day > 0)
        self.day = day-1
        self.hour = hour
        self.minute = minute
        self.second = second
        self.__repr__ = self.__str__

    def __str__(self):
        string = str(self.hour)+":"
        string += str(self.minute)+":"
        string += "{:02}".format(self.second)+" "
        string += self.month_to_str(self.month)+" "
        string += str(self.day+1)+", "
        string += str(self.year)
        return string

    def month_to_str(self, month):
        months = ['January', 'February', 'March', 'April', 'May',
                  'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        return months[month]

    def __lt__(self, other):
        if self.year < other.year:
            return True
        elif self.year > other.year:
            return False

        if self.month < other.month:
            return True
        elif self.month > other.month:
            return False

        if self.day < other.day:
            return True
        elif self.day > other.day:
            return False

        if self.hour < other.hour:
            return True
        elif self.hour > other.hour:
            return False

        if self.minute < other.minute:
            return True
        elif self.minute > other.minute:
            return False

        if self.second < other.second:
            return True
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, Time):
            if (self.year == other.year and
                    self.month == other.month and
                    self.day == other.day and
                    self.hour == other.hour and
                    self.minute == other.minute and
                    self.second == other.second):
                return True
            else:
                return False
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Time):
            # Convert to seconds
            self_seconds = self.convert_to_seconds()
            other_seconds = other.convert_to_seconds()
            # Subtract
            total_seconds = self_seconds - other_seconds
            sign = int(copysign(1, total_seconds))
            total_seconds = abs(total_seconds)
            # Convert back to TimeDelta
            y, total_seconds = divmod(total_seconds, 12*30*24*60*60)
            y = sign * y
            mo, total_seconds = divmod(total_seconds, 30*24*60*60)
            mo = sign * mo
            d, total_seconds = divmod(total_seconds, 24*60*60)
            d = sign * d
            h, total_seconds = divmod(total_seconds, 60*60)
            h = sign * h
            mi, total_seconds = divmod(total_seconds, 60)
            mi = sign * mi
            s = sign * total_seconds
            return TimeDelta(y,mo,d,h,mi,s)
        else:
            return NotImplemented

    def convert_to_seconds(self):
        total_seconds = self.second
        total_seconds += self.minute * 60
        total_seconds += self.hour * (60*60)
        total_seconds += self.day * (60*60*24)
        total_seconds += self.month * (60*60*24*30)
        total_seconds += self.year * (60*60*24*30*12)
        return total_seconds

    def __add__(self, other):
        if isinstance(other, TimeDelta):
            mi, s = divmod(self.second + other.seconds, 60)
            h, mi = divmod(mi + self.minute + other.minutes, 60)
            d, h = divmod(h + self.hour + other.hours, 24)
            mo, d = divmod(d + self.day + other.days, 30)
            y, mo = divmod(mo + self.month + other.months, 12)
            y = y + self.year + other.years
            return Time(y,mo+1,d+1,h,mi,s)
        else:
            return NotImplemented

    def before(self, other):
        return self < other

    def after(self, other):
        return self > other

    def at_same_time_as(self, other):
        return self == other

class TimeKeeper:

    def __init__(self, event_dispatcher):
        self.dispatcher = event_dispatcher
        self.current_time = None
        self.future_events = []

    def handle_time_event(self, event):
        # event.time_taken should be a time_delta object
        self.current_time += event.time_taken
        for event in self.future_events:
            if event.time.before(self.current_time):
                self.future_events.remove(event)
                self.dispatcher.dispatch(event)

    def add_future_event(self, event, time):
        #TODO could keep future_event list sorted?
        event.time = time
        self.future_events.append(event)

if __name__ == "__main__":
    t1 = Time(1000, 10, 25, 13, 20, 0)
    td = TimeDelta(0, 0, 1, 4, 0, 0)
    print "Time 1: " + str(t1)
    print "Time delta: " + str(td)
    print "New time: " + str(t1+td)
