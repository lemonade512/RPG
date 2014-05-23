import itemlist

class Player:
    Name = "Player"
    def __init__(self, test = False):
	self.test = test
	self.inventory = [itemlist.testitem]
	self.wisdom = 0
	self.intelligence = 0
	self.strength = 10
	self.charisma = 0
	self.dexterity = 0
	self.constitution = 10
	self.defense = 15
	self.attack = 5
	self.baseattack = 0
	self.stats = (self.strength, self.dexterity, self.constitution,
		      self.wisdom, self.intelligence, self.charisma,
		      self.defense, self.baseattack)
	self.head = ("head", ("None", 0))
	self.chest = ("chest", ("None", 0))
	self.legs = ("legs", ("None", 0))
	self.feet = ("feet", ("None", 0))
	self.weapon = ("weapon", ("None", 0))
	self.equipment = [self.head, self.chest, \
			    self.legs, self.feet, self.weapon]
	self.location = (0, 0)
	self.money = 0
	self.health = self.constitution
	self.maxhealth = self.constitution

    def printStats(self):
	print "Strength:: " + str(self.strength)
	print "Dexterity:: " + str(self.dexterity)
	print "Constitution:: " + str(self.constitution)
	print "Wisdom:: " + str(self.wisdom)
	print "Intelligence:: " + str(self.intelligence)
	print "Charisma:: " + str(self.charisma)
	print "Defense:: " + str(self.defense)
	print "Base Attack:: " + str(self.baseattack)
	print "Money:: " + str(self.money)
	print "Location :: " + str(self.location)

    def printInventory(self):
	for item in self.inventory:
	    print item.name

    def printEquip(self):
	print "Head:: " + str(self.head)
	print "Chest:: " + str(self.chest)
	print "Legs:: " + str(self.legs)
	print "Feet:: " + str(self.feet)
    
    def addInv(self, item):
	self.inventory = self.inventory.append(item)

    def remInv(self, item):
	if item in self.inventory:
	    self.inventory.remove(item)
	else:
	    print "That item is not in inventory"

    def changeStat(self, num, stat, action = "change"):
	if stat == "str":
	    self.changeStr(num, action)
	elif stat == "dex":
	    self.changeDex(num, action)
	elif stat == "con":
	    self.changeCon(num, action)
	elif stat == "wis":
	    self.changeWis(num, action)
	elif stat == "int":
	    self.changeInt(num, action)
	elif stat == "cha":
	    self.changeCha(num, action)
	elif stat == "def":
	    self.changeDef(num, action)
	elif stat == "att":
	    self.changeAtt(num, action)
	else:
	    print "wrong stat to change"

    def changeStr(self, num, action):
	if action == "change":
	    self.strength = num
	elif action == "add":
	    self.strength += num
	elif action == "sub":
	    self.strength -= num
	else:
	    print "Bad action for stat change"

    def changeDex(self, num, action):
	if action == "change":
	    self.dexterity = num
	elif action == "add":
	    self.dexterity += num
	elif action == "sub":
	    self.dexterity -= num
	else:
	    print "Bad action for stat change"

    def changeCon(self, num, action):
	if action == "change":
	    self.constitution = num
	elif action == "add":
	    self.constitution += num
	elif action == "sub":
	    self.constitution -= num
	else:
	    print "Bad action for stat change"

    def changeWis(self, num, action):
	if action == "change":
	    self.wisdom = num
	elif action == "add":
	    self.wisdom += num
	elif action == "sub":
	    self.wisdom -= num
	else:
	    print "Bad action for stat change"

    def changeInt(self, num, action):
	if action == "change":
	    self.intelligence = num
	elif action == "add":
	    self.intelligence += num
	elif action == "sub":
	    self.intelligence -= num
	else:
	    print "Bad action for stat change"

    def changeCha(self, num, action):
	if action == "change":
	    self.charisma = num
	elif action == "add":
	    self.charisma += num
	elif action == "sub":
	    self.charisma -= num
	else:
	    print "Bad action for stat change"

    def changeDef(self, num, action):
	if action == "change":
	    self.defense = num
	elif action == "add":
	    self.defense += num
	elif action == "sub":
	    self.defense -= num
	else:
	    print "Bad action for stat change"

    def changeAtt(self, num, action):
	if action == "change":
	    self.baseattack = num
	elif action == "add":
	    self.baseattack += num
	elif action == "sub":
	    self.baseattack -= num
	else:
	    print "Bad action for stat change"

    def GetHealth(self):
	return self.health

    def LoseHealth(self, amt):
	self.health -= amt

    def GetDefense(self):
	return self.defense

    def UseItem(self, name):
	used = False
	for item in self.inventory:
	    if item.name == name:
		print "This item is in the inventory"
		###################Needs to be revised#################
		###################Use Item############################
		used = True
		return "used"
	if not used:
	    print "That item is not in your inventory."
	    return "not used"

    def GetAttack(self):
	return self.attack

    def GetStrength(self):
	return self.strength
