import time
import random

def Pause(length = .3):
    time.sleep(length)

def RollDie(n):
    roll = random.randint(1,n)
    return roll
