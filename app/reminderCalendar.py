from reminder import Reminder
from reminderTime import ReminderTime
import datetime

class ReminderCalendar:
    def __init__(self):
        self.reminderList = []

    def __str__(self):
        returnString = ""
        for item in self.reminderList:
            returnString += item.__str__() + '\n\n'
        returnString = returnString[0:-2]
        return returnString

    def addReminder(self, reminderToAdd):
        newReminderTime = reminderToAdd.reminderTime
        for i in range(len(self.reminderList)):
            timeOfCurrentItem = self.reminderList[i].reminderTime
            if newReminderTime < timeOfCurrentItem:
                self.reminderList.insert(i, reminderToAdd)
                return reminderToAdd
        self.reminderList.append(reminderToAdd)

    def getTodaysReminders(self): # make it fetch actual time / date
        listToday = []
        now = datetime.datetime.now()
        nowYear = int(str(now.date())[:4])
        nowMonth = int(str(now.date())[5:7])
        nowDate = int(str(now.date())[8:10])
        for reminderItem in self.reminderList:
            timeTemp = reminderItem.reminderTime
            if timeTemp.month == nowMonth and timeTemp.day == nowDate and timeTemp.year == nowYear:
                listToday.append(reminderItem)
        return(listToday)

    def hasConflicts(self, reminderToAdd):
        for reminderItem in self.reminderList:
            if reminderItem.reminderTime.endhour == 0:
                continue
            if reminderToAdd.reminderTime.overlapsWith(reminderItem.reminderTime):
                return True
        return False
