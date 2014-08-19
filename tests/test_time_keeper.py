#!/usr/bin/env python
from RPG.time_keeper import Time, TimeDelta
from nose.tools import *

class TestTime:

    def test_subtract_time(self):
        t1 = Time(1000, 11, 25, 5, 27, 45)
        t2 = Time(1000, 9, 10, 1, 5, 10)
        assert_equal(t1 - t2, TimeDelta(0, 2, 15, 4, 22, 35))

    def test_subtract_time_negative_hour(self):
        t1 = Time(1000, 10, 25, 4, 20, 0)
        t2 = Time(1000, 10, 25, 5, 10, 0)
        assert_equal(t1 - t2, TimeDelta(0, 0, 0, 0, -50, 0))
        assert_equal(t2 - t1, TimeDelta(0, 0, 0, 0, 50, 0))

    def test_subtract_time_negative_day(self):
        t1 = Time(1000, 10, 10, 4, 20, 0)
        t2 = Time(1000, 10, 22, 5, 15, 7)
        assert_equal(t2 - t1, TimeDelta(0, 0, 12, 0, 55, 7))
        assert_equal(t1 - t2, TimeDelta(0, 0, -12, 0, -55, -7))

    def test_add_time(self):
        t1 = Time(1000, 10, 25, 13, 20, 0)
        td = TimeDelta(0, 0, 1, 4, 0, 0)
        assert_equal(t1 + td, Time(1000, 10, 26, 17, 20, 0))

    def test_add_time_overflow(self):
        t1 = Time(1000, 10, 25, 13, 20, 0)
        td = TimeDelta(0, 0, 7, 12, 0, 0)
        assert_equal(t1 + td, Time(1000, 11, 3, 1, 20, 0))

    def test_less_than_time(self):
        t1 = Time(1000, 10, 24, 14, 35, 0)
        t2 = Time(1000, 10, 21, 10, 00, 0)
        assert_true(t2 < t1)

    def test_greater_than_time(self):
        t1 = Time(1000, 10, 23, 14, 35, 0)
        t2 = Time(1000, 10, 21, 10, 00, 0)
        assert_true(t1 > t2)

    def test_time_string_representation(self):
        t = Time(1000, 10, 23, 14, 30, 0)
        assert_equal(str(t), "14:30:00 October 23, 1000")

    def test_time_delta_string_representation(self):
        t = TimeDelta(0, 3, 10, 5, 10, 0)
        string = "Years: 0 Months: 3 Days: 10 Hours: 5"
        string += " Minutes: 10 Seconds: 0"
        assert_equal(str(t), string)

    def test_time_deltas_not_equal(self):
        t1 = TimeDelta(10, 3, 5, 2, 10, 30)
        t2 = TimeDelta(10, 3, 5, 2, 10, 31)
        assert_false(t1 == t2)
        assert_false(t1 == None)

    def test_time_less_than_day(self):
        t1 = Time(1000, 10, 3, 2, 30, 0)
        t2 = Time(1000, 10, 4, 2, 30, 0)
        assert_true(t1 < t2)
        assert_false(t1 > t2)

    def test_time_less_than_hour(self):
        t1 = Time(1000, 10, 3, 1, 30, 0)
        t2 = Time(1000, 10, 3, 2, 30, 0)
        assert_true(t1 < t2)
        assert_false(t2 < t1)
