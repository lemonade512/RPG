from game import *
from statemanager import StateManager
from grid import Grid
import sys

def test():
    testStateManager()
    testGame()
    testGrid()
    testLocation()
    testPlayer()
    testCreature()
    

def testStateManager():
    testSMMenu()
    testSMQuit()

def testSMMenu():
    test_sm = StateManager(True)
    try:
	assert test_sm.Menu("a") == "Play"
	assert test_sm.Menu("b") == "Quit"
	assert test_sm.Menu("jk") == "invalid"
	assert test_sm.Menu("A") == "Play"
	print test_sm.Name + " " + test_sm.Menu.__name__ + \
		"      tests pass"
    except:
	print test_sm.Name + " " + test_sm.Menu.__name__ + \
		"      tests fail"
	print "Unexpacted error", sys.exc_info()[0]

def testSMQuit():
    test_sm = StateManager(True)
    try:
	assert test_sm.Quit() == "Quit"
	print test_sm.Name + " " + test_sm.Quit.__name__ + \
		"      tests pass"
    except:
	print test_sm.Name + " " + test_sm.Quit.__name__ + \
		"      tests fail"
	print "Unexpected error", sys.exc_info()[0]

def testGame():
    testGLoad()
    testGPlay()
    testGQuit()

def testGLoad():
    test_g = Game(True)
    try:
	assert test_g.Load() == "Loading"
	print test_g.Name + " " + test_g.Load.__name__ + \
		"              tests pass"
    except:
	print test_g.Name + " " + test_g.Load.__name__ + \
		"              tests fail"
	print "Unexpected error", sys.exc_info()[0]

def testGPlay():
    test_g = Game(True)
    try:
	msg, p1_loc = test_g.Play("n")
	assert msg == "Playing"
	assert p1_loc == (0,1)
	msg, p1_loc = test_g.Play("s")
	assert msg == "Playing"
	assert p1_loc == (0,0)
	print test_g.Name + " " + test_g.Play.__name__ + \
		"              tests pass"
    except:
	print test_g.Name + " " + test_g.Play.__name__ + \
		"              tests fail"
	print "Unexpected error", sys.exc_info()[0]

def testGQuit():
    test_g = Game(True)
    try:
	assert test_g.Quit() == "Quit"
	print test_g.Name + " " + test_g.Quit.__name__ + \
		"              tests pass"
    except:
	print test_g.Name + " " + test_g.Quit.__name__ + \
		"              tests fail"
	print "Unexpected error", sys.exc_info()[0]

def testGrid():
    test_g = Grid(True)
    try:
	assert test_g.locations[locationlist.l1.point] == \
		locationlist.l1, "Grid A1"
	assert test_g.GetCurrentLocPoint(test_g.testplayer) == (0,0), "Grid A2"
	assert test_g.GetCurrentLocName(test_g.testplayer) == \
						"TestLoc1", "Grid A3"
	testGrGetAdjLocs(test_g)
	testGrMove(test_g)
	testGrGetPossibleMoves(test_g)
	testGrPrintPossibleMoves(test_g)
	print test_g.Name + "                   tests pass"
    except AssertionError, msg:
	print test_g.Name + "                   tests fail"
	print "Assertion error on " + msg.args[0]
    except: 
	print test_g.Name + "                   tests fail"
	print "Unexpected error", sys.exc_info()[0]
	raise

def testGrGetAdjLocs(test_g):
    try:
	assert test_g.GetAdjLocs(test_g.testplayer) == \
		[locationlist.l3.point,locationlist.l5.point,
		 locationlist.l2.point,locationlist.l4.point], "Grid A4"
	assert test_g.GetCurrentLocPoint(test_g.testplayer) == (0,0), "Grid A5"
	print test_g.Name + " " + test_g.GetAdjLocs.__name__ + \
		"        tests pass"
    except:
	print test_g.Name + " " + test_g.GetAdjLocs.__name__ + \
		"        tests fail"
	raise

def testGrMove(test_g):
    try:
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
	print test_g.Name + " " + "Move" + "              tests pass"
    except:
	print test_g.Name + " " + "Move" + "              tests fail"
	raise

def testGrGetPossibleMoves(test_g):
    try:
	test_g.SetLoc(test_g.testplayer, (0,0))
	assert test_g.GetPossibleMoves(test_g.testplayer) == \
		[("e",(1,0)),("w",(-1,0)),("n",(0,1)),("s",(0,-1))], "Grid A10"
	print test_g.Name + " GetPossMoves      tests pass"
    except:
	print test_g.Name + " GetPossMoves      tests fail"
	raise

def testGrPrintPossibleMoves(test_g):
    try:
	assert test_g.PrintPossibleMoves(test_g.testplayer) == \
		"e, w, n, s, ", "Grid A11"
	print test_g.Name + " PrintPossMoves    tests pass"
    except:
	print test_g.Name + " PrintPossMoves    tests fail"
	raise

def testLocation():
    try:
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
	testLocTown()
	print "Location               tests pass"
    except AssertionError, msg:
	print "Location               tests fail"
	print "Assertion error " + msg.args[0]
    except:
	print "Location               tests fail"
	print "Unexpected error", sys.exc_info()[0]

def testLocTown():
    try:
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
	print "Location Town          tests pass"
    except:
	print "Location Town          tests fail"
	raise

def testPlayer():
    try:
    	tp1 = Player(True)
       	assert tp1.stats == (10,0,10,0,0,0,15,0)
	assert tp1.location == (0,0)
	assert tp1.money == 0
	assert tp1.equipment == [("head", ("None", 0)), ("chest", ("None", 0)),
				 ("legs", ("None", 0)), ("feet", ("None", 0)),
				 ("weapon", ("None", 0))]
	tp1.changeStat(5,"str")
	assert tp1.strength == 5
	tp1.changeStat(2,"str", "add")
	assert tp1.strength == 7
	tp1.changeStat(1,"str", "sub")
	assert tp1.strength == 6
	tp1.changeStat(4,"def")
	assert tp1.defense == 4
	print "Player                 tests pass"
    except:
	print "Player                 tests fail"
	print "Unexpected error", sys.exc_info()[0]
	raise

def testCreature():
    try:
	tc1 = Creature()
	assert tc1.GetHealth() == 10
	tc1.LoseHealth(5)
	assert tc1.GetHealth() == 5
	assert tc1.GetName() == "Generic Creature"
	assert tc1.GetDex() == 5
	assert tc1.GetDefense() == 10
	assert tc1.GetAttack() == 2
	assert tc1.GetStrength() == 6
	print "Creature               tests pass"
    except:
	print "Creature               tests fail"
	print "Unexpected error", sys.exc_info()[0]
	raise

test()
