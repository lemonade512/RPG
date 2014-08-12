#!/usr/bin/env python
from RPG.player import Player

def testPlayer():
    tp1 = Player(True)
    assert tp1.stats == (10,0,10,0,0,0,15,0)
    assert tp1.location == (0,0)
    assert tp1.money == 0
    assert tp1.equipment == [("head", ("None", 0)), ("chest", ("None", 0)),
                             ("legs", ("None", 0)), ("feet", ("None", 0)),
                             ("weapon", ("None", 0))]
