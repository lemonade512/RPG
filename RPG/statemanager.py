from game import Game
import sys

class StateManager:
    Name = "StateManager"

    def __init__(self, test = False):
	self.state = "Menu"
	self.test = test

    def Menu(self, user_choice = ""):
	if not self.test:
    	    print "Hello Adventurerer and welcome to my awesome game."
    	    print "[a] Play"
    	    print "[b] Quit"
	while True:
	    if not self.test:
	       	user_choice = raw_input("What would you like to do?  ")
    	    if user_choice.lower() == "a":
    		return "Play"
    	    elif user_choice.lower() == "b":
    		return "Quit"
    	    else:
		if self.test:
		    return "invalid"
		else:
		    print "You have entered an invalid choice. Choose [a] or [b]."

    def Play(self):
	game = Game()
    	game.Load()
	game.Play()
	state = game.Quit()
	return state

    def Quit(self):
	if not self.test:
	    print "Goodbye!!"
	return "Quit"

def StartManager():
    sm = StateManager()
    while sm.state is not "Quit":
       	if sm.state == "Menu":
    	    sm.state = sm.Menu()
       	elif sm.state == "Play":
    	    sm.state = sm.Play()
       	elif sm.state == "Quit":
    	    sm.state = sm.Quit()
       	else:
    	    print "invalid state"
    	    print sm.state
    	    sm.state = "Quit"
