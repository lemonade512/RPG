from RPG.grid import Grid
import RPG.locationlist as locationlist

def test_Grid():
    test_g = Grid(True)
    assert test_g.locations[locationlist.l1.point] == \
            locationlist.l1, "Grid A1"
    assert test_g.GetCurrentLocPoint(test_g.testplayer) == (0,0), "Grid A2"
    assert test_g.GetCurrentLocName(test_g.testplayer) == \
						"TestLoc1", "Grid A3"

def test_GrGetAdjLocs():
    test_g = Grid(True)
    assert test_g.GetAdjLocs(test_g.testplayer) == \
            [locationlist.l3.point,locationlist.l5.point,
             locationlist.l2.point,locationlist.l4.point], "Grid A4"
    assert test_g.GetCurrentLocPoint(test_g.testplayer) == (0,0), "Grid A5"

def test_GrMove():
    test_g = Grid(True)
    test_g.MoveNorth(test_g.testplayer)
    assert test_g.testplayer.location == (0,1), "Grid A6"
    test_g.MoveEast(test_g.testplayer)
    assert test_g.testplayer.location == (1,1), "Grid A7"
    test_g.MoveSouth(test_g.testplayer)
    test_g.MoveSouth(test_g.testplayer)
    assert test_g.testplayer.location == (1,-1), "Grid A8"
    test_g.MoveWest(test_g.testplayer)
    test_g.MoveWest(test_g.testplayer)
    assert test_g.testplayer.location == (-1,-1), "Grid A9"

def test_GrGetPossibleMoves():
    test_g = Grid(True)
    test_g.SetLoc(test_g.testplayer, (0,0))
    assert test_g.GetPossibleMoves(test_g.testplayer) == \
            [("e",(1,0)),("w",(-1,0)),("n",(0,1)),("s",(0,-1))], "Grid A10"

def test_GrPrintPossibleMoves():
    test_g = Grid(True)
    assert test_g.PrintPossibleMoves(test_g.testplayer) == \
            "e, w, n, s, ", "Grid A11"
