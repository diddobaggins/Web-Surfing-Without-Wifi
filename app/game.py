class game:

    def __init__(self):
        self.turn = 0

    def getTurn(self):
        return self.turn

    def move(self, params):
        if self.turn == 0:
            self.turn += 1
            return "What is your name, adventurer?"
        elif self.turn == 1:
            if len(params) > 1:
                self.name = params[1]
                self.turn += 1
                return ("Greetings, {}. Let us go on a quest!\n".format(self.name) +
                        "You find yourself on the edge of a dark forest.\n"
                        "Can you find your way through?\n\n"
                        "Would you like to step into the forest?\nyes/no")
            else:
                return "Please, could you tell me your name?"
        elif self.turn == 2:
            if len(params) > 1 and params[1].lower() == "yes":
                self.turn += 1
                return ("You head into the forest. You hear crows cawwing in the distance.\n"
                        "To your left, you see a bear.\n"
                        "To your right, there is more forest.\n"
                        "There is a rock wall directly in front of you.\n"
                        "Behind you is the forest exit.\n\n"
                        "What direction do you move?\nleft/right/forward/backward\n")
            elif len(params) > 1 and params[1].lower() == "no":
                self.turn = 4
                return "You are not ready for this quest. Goodbye, " + self.name + "."
            else:
                return "I didn't understand that. Please say yes or no."
        elif self.turn == 3:
            if len(params) > 1 and params[1].lower() == "left":
                self.turn += 1
                return "The bear eats you. Farewell, " + self.name + "."
            elif len(params) > 1 and params[1].lower() == "right":
                return ("You head deeper into the forest. You hear more crows cawwing "
                        "in the distance.\nTo your left, you see a bear.\n"
                        "To your right, there is more forest.\n"
                        "There is a rock wall directly in front of you.\n"
                        "Behind you is the forest exit.\n\n"
                        "What direction do you move?\nleft/right/forward/backward\n")
            elif len(params) > 1 and params[1].lower() == "forward":
                return "You cannot scale the wall."
            elif len(params) > 1 and params[1].lower() == "backward":
                self.turn += 1
                return "You leave the forest. Goodbye, " + self.name + "."
            else:
                return "I didn't understand that. Please say left, right, forward, or backward."
