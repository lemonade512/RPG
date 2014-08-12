from RPG.statemanager import StateManager

def test_SMMenu():
    test_sm = StateManager(True)
    assert test_sm.Menu("a") == "Play"
    assert test_sm.Menu("b") == "Quit"
    assert test_sm.Menu("jk") == "invalid"
    assert test_sm.Menu("A") == "Play"

def test_SMQuit():
    test_sm = StateManager(True)
    assert test_sm.Quit() == "Quit"
