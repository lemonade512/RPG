from grid import *
from battle import *
import tools

class Game:
    Name = "Game"
    def __init__(self, test = False):
	self.test = test
	self.grid = Grid(test)
    
    #Available to later initiate necessary files
    def Load(self):
	if not self.test:
	    print "Game is loading"
	    print ""
	return "Loading"
    
    #Primary game loop and movement logic
    def Play(self, user_choice = ""):
	is_playing = True
	while is_playing:
	    if not self.test:
		tools.Pause()
    		print "You are at location:: " + \
    			str(self.grid.GetCurrentLocPoint(self.grid.p1))
    		print "The name of this location is:: " + \
    			self.grid.GetCurrentLocName(self.grid.p1)
		curr_loc = self.grid.GetCurrentLoc(self.grid.p1)
		if curr_loc.CheckForBattle() == "battle":
		    battle = Battle()
		    battle.StartBattle()
		    print "Your health is:: " + str(player.health)
		    if self.grid.p1.GetHealth() <= 0:
			print "You have died"
			is_playing = False
			break
		curr_loc.Start()
	    poss_moves = self.grid.GetPossibleMoves(self.grid.p1)
	    moves_str = self.grid.PrintPossibleMoves(self.grid.p1)
	    good_choice = False
	    count = 0
	    while not good_choice:
		if self.test:
		    count += 1
		if not self.test:
		    user_choice = raw_input("Enter choice: ")
		    print ""
		if user_choice.lower() == "q":
		    is_playing = False
		    good_choice = True
		else:
		    good_choice = self.CheckChoice(user_choice, moves_str)
		    if count == 1: user_choice = "q"
		    if not good_choice:
			print "That is an invalid location. Try again."
    	return ("Playing", self.grid.p1.location)
    
    #Used in game loop for movement checking
    def CheckChoice(self, user_choice, poss_moves):
	if user_choice not in poss_moves:
	    return
	elif user_choice == "e":
	    self.grid.MoveEast(self.grid.p1)
	    return True
	elif user_choice == "w":
	    self.grid.MoveWest(self.grid.p1)
	    return True
	elif user_choice == "n":
	    self.grid.MoveNorth(self.grid.p1)
	    return True
	elif user_choice == "s":
	    self.grid.MoveSouth(self.grid.p1)
	    return True
	else:
	    print "What?????"
	    return False

    def Quit(self):
	if not self.test:
	    print "Game is quitting"
	return "Quit"
