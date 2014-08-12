#!/usr/bin/env python
from RPG.location import Town, Location

def test_Location():
    t_loc1 = Location((0,0), "Test1", True)
    t_loc2 = Location((1,2), "Test2")
    assert t_loc1.point == (0,0)
    assert t_loc1.Name == "Test1"
    assert t_loc1.test == True
    assert t_loc1.danger == 10
    assert t_loc1.Start() == "Location started"
    assert t_loc1.CheckForBattle() == "safe"
    assert t_loc1.CheckForBattle(0) == "battle"
    assert t_loc1.description == "A blank spot of land"
    assert t_loc2.test == False

def test_LocTown():
    t_tow1 = Town((0,0), "TestTown1", True)
    t_tow2 = Town((1,2), "TestTown2")
    assert t_tow1.point == (0,0), "Town A1"
    assert t_tow1.Name == "TestTown1", "Town A2"
    assert t_tow1.test == True, "Town A3"
    assert t_tow1.danger == 1, "Town A4"
    assert t_tow1.Start() == "Town started", "Town A5"
    assert t_tow1.CheckForBattle() == "safe", "Town A6"
    assert t_tow1.CheckForBattle(2) == "safe", "Town A7"
    assert t_tow1.CheckForBattle(1) == "battle", "Town A8"
    assert t_tow2.test == False, "Town A9"
    assert t_tow1.Potions() == "potions"
    assert t_tow1.Weapons() == "weapons"
    assert t_tow1.Armor() == "armor"
    assert t_tow1.description == "Just a simple town"
    t_tow1.setDescription("Not just a simple town")
    assert t_tow1.description == "Not just a simple town"
