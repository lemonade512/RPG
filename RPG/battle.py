from characterlist import *
import tools
import copy

class Battle:
    Name = "Battle"
    def __init__(self, test = False):
        self.test = test

    #1)Starts battle and initiates creature
    #2)Get's user input
    #3)Performs battle logic
    #4)Checks for end of battle
    #5)Prints updates for player
    def StartBattle(self):
        print ""
        tools.Pause()
        creature = self.ChooseCreature()
        print "You are fighting a(n) " + creature.GetName()
        print "Creature's health:: " + str(creature.GetHealth())
        print ""
        fighting = True
        while fighting == True:
            print "Choose an action:: "
            print "(a) Attack"
            print "(b) Use Item"
            print "(c) Flee"
            while True:
                player_choice = raw_input("Choice::")
                if player_choice == "a":
                    fighting = self.Attack(creature, "p")
                    break
                elif player_choice == "b":
                    fighting = self.UseItem(creature)
                    break
                elif player_choice == "c":
                    fighting = self.Flee(creature)
                    break
                else:
                    print "That is an incorrect choice"
                tools.Pause()
                print ""
                if creature.health > 0:
                    fighting = self.Attack(creature, "c")
                else:
                    fighting = False

    #Attacker = 'p' or 'c'
    #Rolls d20, adds attackers attack, updates stats
    #Returns False if creature or player is dead and true if both alive
    def Attack(self, creature, attacker):
        if attacker == "c":
            roll = tools.RollDie(20)
            roll += creature.GetAttack()
            print "Creature attack roll:: " + str(roll)
            if roll > player.GetDefense():
                dmg = tools.RollDie(creature.GetStrength())
                player.LoseHealth(dmg)
                print "You have lost " + str(dmg) + " health."
                print "Your health is now: " + str(player.health)
            else:
                print "The creature swings and misses."
            tools.Pause()
            print ""
        elif attacker == "p":
            roll = tools.RollDie(20) + player.GetAttack()
            print "Your attack roll:: " + str(roll)
            if roll > creature.GetDefense():
                dmg = tools.RollDie(player.GetStrength())
                creature.LoseHealth(dmg)
                print "You have dealt " + str(dmg) + " damage."
                print "The creature's health is now: " + str(creature.GetHealth())
            else:
                print "You swing and miss."
        else:
            print "What??"

        if creature.GetHealth() <= 0 or player.health <= 0:
            return False
        else:
            return True

    #Gets input from player (what item),calls player UseItem fn
    #Prints whether the item was used successfully
    def UseItem(self, creature):
        tools.Pause()
        player.printInventory()
        item_choice = raw_input("What would you like to use?")
        outcome = player.UseItem(item_choice)
        if outcome == "used":
            print "You used an item"
        else:
            print "You did not use an item"

    #Rolls d20, checks value against creatures Dex
    #If successful creature loses all health
    #Prints whether the player has been successful
    def Flee(self, creature):
        tools.Pause()
        roll = tools.RollDie(20)
        print roll
        if roll > creature.GetDex():
            creature.LoseHealth(creature.health)
            print "You have fled"
        else:
            print "You could not flee"

    #Currently choses test creature
    def ChooseCreature(self):
        print "You have chosen a creature"
        creature = copy.copy(c1)
        return creature
