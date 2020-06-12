import random
from fileReader import FileReader

class WordSearch:  # add diagonal if time

    def __init__(self, numWords, sides):
        self.wordList = []
        for word in range(numWords):
            tempWord = FileReader.returnRandomLine()
            while len(tempWord) >= sides or (tempWord in self.wordList):
                tempWord = FileReader.returnRandomLine()
            self.wordList.append(tempWord)
        self.sides = sides
        self.wordGrid = []
        for i in range(sides):
            self.wordGrid.append([])
            for j in range(sides):
                self.wordGrid[i].append("")
        self.genGrid()

    def __str__(self):
        returnString = "------------\n"
        for i in range(self.sides):
            for j in range(self.sides):
                returnString += self.wordGrid[i][j]
                returnString += "\t"
            returnString += '\n'
        returnString += '\n\n'
        returnString += "Find the words: "
        for item in self.wordList:
            returnString += item + " "
        return returnString

    def willFit(self, coor1, coor2, orientate, dir, word):
        if orientate == 0: # horizontal
            if dir == 0: # forward
                if coor2 + len(word) <= self.sides:
                    iter = 0
                    for letter in range(coor2, coor2 + len(word)):
                        if self.wordGrid[coor1][letter] != "" and self.wordGrid[coor1][letter] != word[iter]:
                            return False
                        iter+=1
                    return True
                return False
            if dir == 1: # backward
                if coor2 - len(word) >= -1:
                    iter = 0
                    for letter in range(coor2, coor2 - len(word), -1):
                        if self.wordGrid[coor1][letter] != "" and self.wordGrid[coor1][letter] != word[iter]:
                            return False
                        iter+=1
                    return True
                return False
        if orientate == 1: # vertical
            if dir == 0: # down
                if coor1 + len(word) <= self.sides:
                    iter = 0
                    for letter in range(coor1, coor1 + len(word)):
                        if self.wordGrid[letter][coor2] != "" and self.wordGrid[letter][coor2] != word[iter]:
                            return False
                        iter+=1
                    return True
                return False
            if dir == 1:
                if coor1 - len(word) >= -1:
                    iter = 0
                    for letter in range(coor1, coor1 - len(word), -1):
                        if self.wordGrid[letter][coor2] != "" and self.wordGrid[letter][coor2] != word[iter]:
                            return False
                        iter+=1
                    return True
                return False

    def insertWord(self,coor1, coor2, orientate, dir, word):
        if orientate == 0:
            if dir == 0:
                iter = 0
                for letter in range(coor2, coor2 + len(word)):
                    self.wordGrid[coor1][letter] = word[iter]
                    iter+=1
            if dir == 1:
                iter = 0
                for letter in range(coor2, coor2 - len(word), -1):
                    self.wordGrid[coor1][letter] = word[iter]
                    iter+=1
        if orientate == 1:
            if dir == 0:
                iter = 0
                for letter in range(coor1, coor1 + len(word)):
                    self.wordGrid[letter][coor2] = word[iter]
                    iter+=1
            if dir == 1:
                iter = 0
                for letter in range(coor1, coor1 -  len(word), -1):
                    self.wordGrid[letter][coor2] = word[iter]
                    iter+=1

    def genGrid(self):
        for word in self.wordList:
            coor1 = random.randint(0, self.sides-1) # python should give us a do while loop : (
            coor2 = random.randint(0, self.sides-1)
            orientate = random.randint(0, 1)
            dir =  random.randint(0, 1)
            while self.willFit(coor1, coor2, orientate, dir, word) == False:
                coor1 = random.randint(0, self.sides-1)
                coor2 = random.randint(0, self.sides-1)
                orientate = random.randint(0, 1)
                dir =  random.randint(0, 1)
            self.insertWord(coor1, coor2, orientate, dir, word)
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        for i in range(self.sides):
            for j in range(self.sides):
                if self.wordGrid[i][j] == "":
                    self.wordGrid[i][j] = alphabet[random.randint(0, 25)]
