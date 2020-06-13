import random

class FileReader:

    def returnRandomLine():
        lines = open('app/text.txt').readlines()
        return lines[random.randint(0, len(lines))][:-1]
