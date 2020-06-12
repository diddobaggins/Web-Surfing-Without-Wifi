import threading
import time
from tamagotchi import Tamagotchi

def tamagotchiRun():
    global tamagotchiBaby
    while tamagotchiBaby.isDead == False:
        tamagotchiBaby.stepTamagotchi()
        print(tamagotchiBaby)

def main():
    global tamagotchiBaby
    tamagotchiBaby = Tamagotchi("baby")
    thread = threading.Thread(target=tamagotchiRun)
    thread.start()
    while tamagotchiBaby.isDead == False:
        command = input("What would you like to do?")
        if tamagotchiBaby.isDead == True:
            break
        if command == "feed":
            print(tamagotchiBaby.feedTamagotchi())
        if command == "scold":
            print(tamagotchiBaby.scoldTamagotchi())
        if command == "play":
            print(tamagotchiBaby.playTamagotchi())
        if command == "clean":
            tamagotchiBaby.cleanTamagotchi()
        if command == "sleep":
            print(tamagotchiBaby.sleepTamagotchi())
    print(tamagotchiBaby.deathNote)

main()
