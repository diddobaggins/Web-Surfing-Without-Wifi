import datetime
import random
import time
now = datetime.datetime.now()

class Tamagotchi: # yikes o

    def __init__(self, name):
        self.sleepTimer = 100
        self.sickTimer = 5
        self.age = 0
        self.name = name
        self.condition = {"food": 100, "happy": 100, "energy": 100, "health": 100, "discipline": 0}
        self.isDead = False
        self.isSick = False
        self.isAsleep = False
        self.pooDroppings = 0
        self.expression = "O"
        self.drawing = "O"
        self.deathNote = ""

    def __str__(self):
        returnString = ""
        returnString += "food meter: " + str(self.condition["food"]) + '\n'
        returnString += "happy meter: " + str(self.condition["happy"]) + '\n'
        returnString += "energy meter: " + str(self.condition["energy"]) + '\n'
        returnString += "health meter: " + str(self.condition["health"]) + '\n'
        returnString += self.drawing
        if self.isSick == True:
            returnString += '\nYour tamagotchi is sick...'
        return returnString

    def capValues(self):
        if self.condition["food"] > 100:
            self.condition["food"] = 100
        if self.condition["happy"] > 100:
            self.condition["happy"] = 100
        if self.condition["energy"] > 100:
            self.condition["energy"] = 100
        if self.condition["health"] > 100:
            self.condition["health"] = 100
        if self.condition["discipline"] < 0:
            self.condition["discipline"] = 0
        if self.pooDroppings<-1:
            self.pooDroppings = 0

    def feedTamagotchi(self):
        if self.isAsleep == False:
            ranNum = random.randint(0, self.condition["discipline"])
            if ranNum == 0:
                return "Your tamagotchi refused to eat!"
            self.condition["food"]+=8
            if self.condition["food"] > 100:
                self.condition["health"]-=20
            self.capValues()

    def scoldTamagotchi(self):
        if self.isAsleep == False:
            ranNum = random.randint(0, 10)
            if ranNum == 0:
                self.condition["happy"]-=30
                self.condition["health"]-=20
                return "You scarred your tamagotchi..."
            self.condition["discipline"]+=1

    def playTamagotchi(self):
        if self.isAsleep == False:
            self.condition["energy"]-=10
            if self.condition["energy"]<0:
                self.isDead = True
            ranNum = random.randint(0, 5)
            if ranNum == 0:
                self.condition["discipline"]-=2
                self.pooDroppings+=1
                self.condition["happy"]+=20
                self.capValues()
                return "Your tamagotchi had fun! A little too much fun..."
            self.condition["happy"]+=10
            self.capValues()

    def cleanTamagotchi(self):
        self.pooDroppings-=1

    def sleepTamagotchi(self):
        if self.condition["discipline"]<3:
            return "You're tamagotchi refused to sleep."
        self.isAsleep = True
        self.sleepTimer = 10
        self.drawing = "zzz"

    def stepTamagotchi(self): # runs every 5  seconds
        self.capValues()
        if self.isAsleep == True:
            self.condition["energy"]+=2
            self.sleepTimer-=1
            if self.sleepTimer == 0:
                self.isAsleep = False
            self.capValues()
        if self.isAsleep == False:
            self.age+=1
            maybePoo = random.randint(0,5)
            if maybePoo == 0:
                self.pooDroppings+=1
            pooDamage = random.randint(self.pooDroppings-2, self.pooDroppings+2)
            self.condition["health"]-=pooDamage*2
            self.condition["food"]-=2
            if self.isSick == True:
                self.condition["health"]-=5
                self.capValues()
                self.sickTimer-=1
                if self.sickTimer == 0:
                    self.isSick = False
            else:
                self.condition["happy"]-=1
                self.condition["energy"]-=1
                healthUp = random.randint(0, (self.condition["happy"] + self.condition["energy"])//30)
                self.condition["health"]+= healthUp
                getSick = random.randint(0, self.condition["energy"] + self.condition["happy"]//2)
                if getSick < 5:
                    self.isSick = True
                    self.sickTimer = 5
            self.capValues()
            if self.condition["happy"] > 90:
                self.expression = "> W <"
            elif self.condition["happy"] > 60:
                self.expression = "0 u 0"
            elif self.condition["happy"] > 40:
                self.expression = "- _ -"
            else:
                self.expression = "T _ T"
            willDieSick = random.randint(0, self.condition["health"]**2)
            willDieStarve = random.randint(0, self.condition["food"]**2)
            if self.age > 100:
                self.isDead = True
                self.deathNote = "Your tamagotchi passed away peacefully <3 YOU WIN!"
                self.expression = "X w X"
            if self.condition["health"]<20 or willDieSick == 0:
                self.isDead = True
                self.deathNote = "Your tamagotchi died of illness."
                self.expression = "X _ X"
            if self.condition["happy"]<10:
                self.isDead = True
                self.deathNote = "Your tamagotchi died of depression."
                self.expression = "X _ X"
            if self.condition["energy"]<10:
                self.isDead = True
                self.deathNote = "Your tamagotchi died of exhaustion."
                self.expression = "X _ X"
            if self.condition["food"]<20 or willDieStarve == 0:
                self.isDead = True
                self.deathNote = "Your tamagotchi died of starvation."
                self.expression = "X _ X"
            self.drawing = self.expression
            self.drawing += "*"*self.pooDroppings
            self.capValues()
        time.sleep(5)
