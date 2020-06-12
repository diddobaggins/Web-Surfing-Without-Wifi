from app.tamagotchi import Tamagotchi
from app.wordSearch import WordSearch
from app.search import search
import os
import pickle
from app.game import game
from app.reminderCalendar import ReminderCalendar
from app.reminder import Reminder
import threading
import time
from app.reminderTime import ReminderTime
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

if not os.path.exists('database'):
    pickle.dump({}, open('database', 'wb'))

app = Flask(__name__)

global reminderStorage
reminderStorage = {}
global tamagotchiGames
tamagotchiGames = {}
global sender
def tamagotchiRun():
    global sender
    while tamagotchiGames[sender].isDead == False:
        tamagotchiGames[sender].stepTamagotchi()


@app.route("/", methods=['GET', 'POST'])
def sms():
    global reminderStorage
    global tamagotchiGames
    global sender
    database = pickle.load(open('database', 'rb'))

    body = request.values.get('Body')
    sender = request.values.get('From')
    params = body.split()

    resp = MessagingResponse()

    if sender not in tamagotchiGames:
        print("OK")
        tamagotchiGames[sender] = False

    if params[0].lower() == 'wordsearch':
        sendWordSearch = WordSearch(5, 7).__str__().upper()
        print(sendWordSearch)
        resp.message(sendWordSearch)

    elif params[0].lower() == "reminders" and len(params) == 1:
        responseMessage = ""
        rc = reminderStorage[sender]
        for item in rc.getTodaysReminders():
            print(item)
            responseMessage += item.__str__()+'\n\n'
        resp.message(responseMessage)


    elif params[0].lower() == 'reminders' and params[1].lower() == 'add':
        try:
            params = params[1:]
            warning = ""
            if sender not in reminderStorage:
                reminderStorage[sender] = ReminderCalendar()
            rc = reminderStorage[sender]
            rTitle = body.split("title:")[1].split("date")[0].rstrip().lstrip()
            if params[1] != "yes":
                rDate = body.split("date:")[1].split("time")[0].rstrip().lstrip()
                if "end:" in params:
                    rTime = body.split("time:")[1].split("end")[0].rstrip().lstrip()
                    rEndTime = body.split("end:")[1].rstrip().lstrip()
                    print(body.split("time:"))
                    rt = ReminderTime(False, int(rDate[0:4]), int(rDate[5:7]), int(rDate[8:]), int(rTime[:2]), int(rTime[3:]), int(rEndTime[:2]), int(rEndTime[3:]))
                    if rc.hasConflicts(Reminder(rTitle, rt)):
                        warning = "\nWarning, your event may have a conflict."
                else:
                    rTime = body.split("time:")[1].rstrip().lstrip()
                    rt = ReminderTime(False, int(rDate[0:4]), int(rDate[5:7]), int(rDate[8:]), int(rTime[:2]), int(rTime[3:]))
            else:
                rDate = body.split("date:")[1].rstrip().lstrip()
                print(rDate)
                rt = ReminderTime(True, int(rDate[0:4]), int(rDate[5:7]), int(rDate[8:]))
            rc.addReminder(Reminder(rTitle, rt))
            resp.message(warning)
            print(reminderStorage)
        except:
            responseMessage = "You may have typed something in wrong!\n\nThe format is: 'reminders add allday title: stringtitle date: yyyy/mm/dd time: (if notallday) hh:mm endtime: (if applicable) hh:mm'\n\nThe time is 24 hour time!"
            resp.message(responseMessage)

    elif params[0].lower() == "reminders" and params[1].lower() == "all":
        rc = reminderStorage[sender]
        resp.message(rc.__str__())

    elif params[0].lower() == "tamagotchi" and len(params) == 1:
        tamagotchiGames[sender] = Tamagotchi("baby")
        print("we good")
        thread = threading.Thread(target=tamagotchiRun)
        thread.start()
        resp.message("You just started a tamagotchi game!")

    elif params[0].lower() == "tamagotchi" and tamagotchiGames[sender] != False:
        command = params[1].lower()
        if command == "feed":
            if tamagotchiGames[sender].feedTamagotchi() != None:
                resp.message("Your tamagotchi refused to eat!")
        if command == "scold":
            if tamagotchiGames[sender].scoldTamagotchi() != None:
                resp.message("You scarred your tamagotchi...")
        if command == "play":
            if tamagotchiGames[sender].playTamagotchi() != None:
                resp.message("Your tamagotchi had fun! A little too much fun...")
        if command == "clean":
            tamagotchiGames[sender].cleanTamagotchi()
        if command == "sleep":
            if tamagotchiGames[sender].sleepTamagotchi() != None:
                resp.message("You're tamagotchi refused to sleep.")
        if tamagotchiGames[sender].isDead:
            resp.message(tamagotchiGames[sender].__str__() + '\n\n' + tamagotchiGames[sender].deathNote)
            tamagotchiGames[sender] = False
        if command == "check":
            resp.message(tamagotchiGames[sender].__str__())

    elif params[0].lower() == "helpme" and len(params) == 1:
        responseMessage = "Here are a list of our possible functions and a short description. To learn more, type 'helpme function_name'\n\n"
        responseMessage += "Reminders:\nAllows you to add and view reminders that may be useful.\n\n"
        responseMessage += "Tamagotchi:\nAllows you to start a game where you take care of a pet. \n\n"
        responseMessage += "Wordsearch:\nGenerates a word search for you to kill time.\n\n"
        responseMessage += "News:\nGet a random headline!\n\n"
        responseMessage += "Google:\nGoogle anything.\n\n"
        responseMessage += "Translate:\nA quick but effective translation.\n\n"
        responseMessage += "Wiki:\nGet a quick snippet of wiki.\n\n"
        responseMessage += "Play:\nA fun adventure game."
        resp.message(responseMessage)

    elif params[0].lower() == "helpme":
        if params[1].lower() == "wordsearch":
            resp.message("Type 'wordsearch' to generate a fun word search!")
        if params[1].lower() == "reminders":
            responseMessage = "Helps you keep track of your reminders.\n\nTo add a reminder, use the format: 'reminders add allday title: stringtitle date: yyyy/mm/dd time: (if notallday) hh:mm endtime: (if applicable) hh:mm'\n\n"
            responseMessage += "put 'yes' in allday if your reminder is for the entire day\n\nhh:mm is in 24 hour time.\n\nIf your reminder has an endtime, we check whether or not it conflicts with other reminders and will let you know if it does.\n\n"
            responseMessage += "To see today's reminders, type 'reminders'\n\nTo see all your reminders, type 'reminders all'\n\n"
            responseMessage += "Example format: 'reminders add title: Father's Day date 2020/06/21 time: 11:00 endtime: 23:00'"
            resp.message(responseMessage)
        if params[1].lower() == "tamagotchi":
            responseMessage = "Type 'tamagotchi' to birth a pet.\n\nYou have to keep it alive until it dies of old age. To see how to interact with it, type 'helpme tamagotchiinteract'\n\n"
            responseMessage += "If you don't take care of it properly, it will die. It is especially dangerous if your tamagotchi gets sick, which it will if its stats are low. But sickness will not kill it, necessarily.\n\n"
            responseMessage += "This game does have chance elements, but your diligence will still matter a lot. Happy parenting!\n\n"
            responseMessage += "Tip: If your tamagotchi is misbehaving... scold it!"
            resp.message(responseMessage)
        if params[1].lower() == "tamagotchiinteract":
            responseMessage = "'tamagotchi feed': Feed your tamagotchi. Sometimes though, it might not listen.\n\n"
            responseMessage += "'tamagotchi scold': Discipline your tamagotchi. This might have dire effects however.\n\n"
            responseMessage += "'tamagotchi play': Mental health is important. Keep your tamagotchi happy!\n\n"
            responseMessage += "'tamagotchi clean': If your tamagotchi has * next to it, it has pooped. Do this to remove a poop. It's poop may affect its health.\n\n"
            responseMessage += "'tamagotchi sleep': Your tamagotchi may be tired. Make sure to let it rest!\n\n"
            responseMessage += "'tamagotchi check': This is important. It will show your tamagotchi's current stats."
            resp.message(responseMessage)
        if params[1].lower() == "news":
            resp.message("Type 'news' for a cool headline!")
        if params[1].lower() == "google":
            resp.message("Type 'google ' followed by your search term to see Google's top result.")
        if params[1].lower() == "translate":
            resp.message("Send a message in the following format: 'translate CODE TEXT' where "
                         "CODE is the ISO 639-1 code for the language wanted ("
                         "found at http://www.loc.gov/standards/iso639-2/php/code_list.php) "
                         "and TEXT is the message to be translated.")
        if params[1].lower() == "wiki":
            resp.message("Type 'wiki ' followed by your search term.")
        if params[1].lower() == "play":
            resp.message("Type 'play' to see an interesting game. Type 'play' in front of all the games commands. (If the game asks for your name, type 'play name')")

    elif params[0].lower() == 'google':
        if len(params) > 1:
            result = search.google(body[7:])
            resp.message("Here is Google's top result:\n" + result)
        else:
            resp.message("Please enter your search terms after 'google'.")
    elif params[0].lower() == 'translate':
        if len(params) >= 3:
            msg = search.translate(" ".join(params[2:]), params[1].lower())
            if msg == "":
                resp.message("An error occurred during translation.")
            else:
                resp.message(msg)
        else:
            resp.message("Send a message in the following format: 'translate CODE TEXT' where "
                         "CODE is the ISO 639-1 code for the language wanted ("
                         "found at http://www.loc.gov/standards/iso639-2/php/code_list.php) "
                         "and TEXT is the message to be translated.")
    elif params[0].lower() == 'wiki':
        if len(params) > 1:
            result = search.wiki(body[5:])
            if len(result) < 1530:
                resp.message("Information from Wikipedia:\n" + result)
            else:
                resp.message("Information from Wikipedia:\n" + result[:1525])
                result = result[1525:]
                while len(result) >= 1530:
                    resp.message(result[:1525])
                    result = result[1525:]
                resp.message(result)
        else:
            resp.message("Please enter your search terms after 'wiki'.")
    elif params[0].lower() == 'weather':
        if len(params) > 1:
            resp.message(search.weather(body[8:]))
        else:
            resp.message(search.weather())
    elif params[0].lower() == 'news':
        if len(params) > 1:
            resp.message(search.news(body[5:]))
        else:
            resp.message(search.news(""))
    elif params[0].lower() == 'play':
        if 'players' not in database:
            database['players'] = {}
        players = database['players']
        if sender not in players:
            players[sender] = game()
        resp.message(players[sender].move(params))
        if players[sender].getTurn() == 4:
            del players[sender]
    # Update database file
    else:
        resp.message("Hello, your message was not a known command. To check out what we do, type 'helpme'")


    with open('database', 'wb') as f:
        pickle.dump(database, f)

    return str(resp)
