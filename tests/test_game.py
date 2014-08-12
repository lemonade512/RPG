from RPG.game import *

def test_GLoad():
    test_g = Game(True)
    assert test_g.Load() == "Loading"

def test_GPlay():
    test_g = Game(True)
    msg, p1_loc = test_g.Play("n")
    assert msg == "Playing"
    assert p1_loc == (0,1)
    msg, p1_loc = test_g.Play("s")
    assert msg == "Playing"
    assert p1_loc == (0,0)

def test_GQuit():
    test_g = Game(True)
    assert test_g.Quit() == "Quit"
