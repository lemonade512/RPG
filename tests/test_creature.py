#!/usr/bin/env python
from RPG.creature import Creature

def test_Creature():
    tc1 = Creature()
    assert tc1.GetHealth() == 10
    tc1.LoseHealth(5)
    assert tc1.GetHealth() == 5
    assert tc1.GetName() == "Generic Creature"
    assert tc1.GetDex() == 5
    assert tc1.GetDefense() == 10
    assert tc1.GetAttack() == 2
    assert tc1.GetStrength() == 6
