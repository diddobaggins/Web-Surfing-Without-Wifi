from reminderTime import ReminderTime # if time, move reminder up a day if its not deleted, and also code reminder delete

class Reminder:
    def __init__(self, reminderName, reminderTime, reminderDescription=""):
        self.reminderName = reminderName
        self.reminderTime = reminderTime
        self.reminderDescription = reminderDescription

    def __str__(self):
        if self.reminderDescription == "":
            return 'Reminder: {} \nTime: {}'.format(self.reminderName, self.reminderTime.__str__())
        return 'Reminder: {} \nTime: {} \nDescription: {}'.format(self.reminderName, self.reminderTime.__str__(), self.reminderDescription)
