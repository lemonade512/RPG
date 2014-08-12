import tools
import characterlist

class Location:

    def __init__(self, point, name, test = False, text = "", danger = 10):
	self.Name = name
	self.point = point
	self.test = test
	self.danger = danger
	self.text = "Welcome to " + self.Name
	self.description = "A blank spot of land"
    
    #Prints location text and description
    def Start(self):
	if not self.test:
	    print self.text
	    self.printDescription()
	return "Location started"
    
    #Logic to check for a battle
    #Rolls a 100-sided die and checks it against danger value
    def CheckForBattle(self, roll=100):
	if not self.test:
	    die_roll = tools.RollDie(100)
	else: die_roll = roll

	if die_roll > self.danger:
	    return "safe"
	else:
	    if not self.test:
		print "You entered a battle"
	    return "battle"
    
    #Sets location description
    def setDescription(self, des):
	self.description = des
    
    #Prints location description
    def printDescription(self):
	print self.description
    
class Path(Location):
    
    def __init__(self, point, name, test = False, text = "", danger = 10):
	Location.__init__(self, point, name, test)
	self.danger = danger
	self.description = "A typical path"

class Cave(Location):
    def __init__(self, point, name, test = False, text = "", danger = 50):
	Location.__init__(self, point, name, test)
	self.danger = danger
	self.description = "A scary cave"

class Town(Location):

    def __init__(self, point, name, test = False, text = "", danger = 1):
	Location.__init__(self, point, name, test)
	self.danger = danger
	self.description = "Just a simple town"
	self.potionStock = []
	self.armorStock = []
	self.weaponStock = []
    
    #Logic for town with potions,weapons, and armor shop
    def Start(self):
	self.CheckForBattle()
	if not self.test:
	    print self.text
	    tools.Pause()
	    print "You are in a town"
	    self.printDescription()
	    tools.Pause(.5)
	    will_stay = True
	    while will_stay:
		tools.Pause()
		print ""
    		print "Would you like to visit::"
    		print "[a] Potions shop"
    		print "[b] Weapons shop"
    		print "[c] Armor shop"
    		print "[d] Exit"
    		user_choice = raw_input()
    		if user_choice == "a":
		    tools.Pause()
    		    self.Potions()
    		elif user_choice == "b":
		    tools.Pause()
    		    self.Weapons()
    		elif user_choice == "c":
		    tools.Pause()
    		    self.Armor()
    		elif user_choice == "d":
		    will_stay = False
		    print ""
    		    print "Goodbye!"
		else:
		    print "That is an invalid choice"
	return "Town started"
    
    #Potion shop logic
    def Potions(self):
	if not self.test:
	    print ""
    	    print "In potions shop"
	return "potions"
    
    #Weapons shop logic
    def Weapons(self):
	if not self.test:
    	    print ""
    	    print "In weapons shop"
	return "weapons"
    
    #Armor shop logic
    def Armor(self):
	if not self.test:
    	    print ""
    	    print "In armor shop"
	return "armor"
