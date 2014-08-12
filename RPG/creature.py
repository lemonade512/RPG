class Creature:
    Name = "Generic Creature"
    #Defines creature attributes
    def __init__(self, h = 10, att = 2, defense = 10, strength = 6, dex = 5):
	self.health = h
	self.attack = att
	self.defense = defense
	self.strength = strength
	self.dexterity = dex
    
    #Reduces creature's health by n
    def LoseHealth(self, n):
	self.health -= n
    
    #Returns health
    def GetHealth(self):
	return self.health
    
    #Returns name
    def GetName(self):
	return self.Name
    
    #Retuurns dexterity
    def GetDex(self):
	return self.dexterity

    #Returns defense
    def GetDefense(self):
	return self.defense
    
    #Returns strength
    def GetStrength(self):
	return self.strength

    #Returns attack
    def GetAttack(self):
	return self.attack
