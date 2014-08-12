import locationlist
from location import *
from player import *
import sys

class Grid:
    Name = "Grid"
    #Initiates player with location (0,0) and loads locations
    def __init__(self, test = False):
    	self.p1 = characterlist.player
	self.p1.location = (0,0)
	self.test = test
	self.locations = locationlist.locs
	if test:
	    self.testplayer = Player(test)
	    self.testplayer.location = (0,0)
	    self.p1 = self.testplayer
    	    self.locations = locationlist.testlocs
    
    #Gets players current location from location list
    def GetCurrentLoc(self, player):
	loc = self.locations[self.GetCurrentLocPoint(player)]
	return loc
    
    #Returns players location point (x,y)
    def GetCurrentLocPoint(self, player):
	return player.location

    #Returns the name of players current location
    def GetCurrentLocName(self, player):
	loc = self.locations[self.GetCurrentLocPoint(player)]
	return loc.Name

    #Returns list of adjacent locations
    def GetAdjLocs(self, player):
	locs = []
	x,y = player.location
	if self.locations.get((x+1,y)):
	    locs.append((x+1,y))
	if self.locations.get((x-1,y)):
	    locs.append((x-1,y))
	if self.locations.get((x,y+1)):
	    locs.append((x,y+1))
	if self.locations.get((x,y-1)):
	    locs.append((x,y-1))
	return locs

    #Returns list of possible m,ove locations
    #In the form of tuples (direction, point) in order of e,w,n,s
    def GetPossibleMoves(self, player):
   	locs = self.GetAdjLocs(player)
	poss_moves = []
	for loc in locs:
	    x0, y0 = player.location
	    x,y = loc
	    if x0 - x == 1 and y0 == y:
		poss_moves.append(("w",loc))
	    elif x0-x == -1 and y0 == y:
		poss_moves.append(("e",loc))
	    elif x0 == x and y0 - y == 1:
		poss_moves.append(("s",loc))
	    elif x0 == x and y0 - y == -1:
		poss_moves.append(("n", loc))
	    else:
		print "invalid adjacent location"
	return poss_moves

    def PrintPossibleMoves(self, player):
	poss_moves = self.GetPossibleMoves(player)
	dir_str = ""
	for move in poss_moves:
	    if move[0] == "n":
		dir_str = dir_str + "n, "
	    elif move[0] == "e":
		dir_str = dir_str + "e, "
	    elif move[0] == "s":
		dir_str = dir_str + "s, "
	    elif move[0] == "w":
		dir_str = dir_str + "w, "
	    else:
		print "Wrong input letter"
		
	if not self.test:
	    print "You can move:: " + dir_str + "or you can (q)uit"

	return dir_str
    
    #Moves player North
    def MoveNorth(self, player):
	x,y = player.location
	self.SetLoc(player, (x,y+1))

    #Moves player East
    def MoveEast(self, player):
	x,y = player.location
	self.SetLoc(player, (x+1,y))
    
    #Moves player South
    def MoveSouth(self, player):
	x,y = player.location
	self.SetLoc(player, (x,y-1))
    
    #Moves player West
    def MoveWest(self, player):
	x,y = player.location
	self.SetLoc(player, (x-1,y))
    
    #Sets player location to point (x,y)
    def SetLoc(self, player, point):
	player.location = point
