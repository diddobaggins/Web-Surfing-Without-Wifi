class ReminderTime:
    def __init__(self, allDay, year, month, day, hour = 0, minute = 0, endhour = 0, endminute = 0):
        self.allDay = allDay
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.endhour = endhour
        self.endminute = endminute
        self.starttime = str(hour) + ":" + str(minute).zfill(2)
        self.endtime = str(endhour) + ":" + str(endminute).zfill(2)

    def __str__(self):
        if self.allDay:
            return '{}/{}/{}'.format(self.year, str(self.month).zfill(2), str(self.day).zfill(2))
        if self.endhour == 0:
            return '{}/{}/{} {}'.format(self.year, str(self.month).zfill(2), str(self.day).zfill(2), self.starttime)
        return '{}/{}/{} {}-{}'.format(self.year, str(self.month).zfill(2), str(self.day).zfill(2), self.starttime, self.endtime)

    def __lt__(self, other):
        if self.year < other.year:
            return True
        if self.year > other.year:
            return False
        if self.month < other.month:
            return True
        if self.month > other.month:
            return False
        if self.day < other.day:
            return True
        if self.day > other.day:
            return False
        if self.allDay or other.allDay:
            returnTrue
        if self.hour < other.hour:
            return True
        if self.hour > other.hour:
            return False
        if self.minute < other.minute:
            return True
        if self.minute > other.minute:
            return False

    def __gt__(self, other):
        if self.year > other.year:
            return True
        if self.year < other.year:
            return False
        if self.month > other.month:
            return True
        if self.month < ohter.month:
            return False
        if self.day > other.day:
            return True
        if self.day < other.day:
            return False
        if self.allDay or other.allDay:
            return True
        if self.hour > other.hour:
            return True
        if self.hour < other.hour:
            return False
        if self.minute > other.minute:
            return True
        if self.minute < other.minute:
            return False

    def __eq__(self, other):
        if self.year == other.year and self.month == other.month and self.day == other.day and self.hour == other.hour and self.minute == other.minute:
            return True
        return False

    def overlapsWith(self, timeOther): # returns True if two reminders overlap, False if they don't
        if self.day == timeOther.day and self.month == timeOther.month and self.year == timeOther.year: # change this to use > < if time
            if self.allDay:
                return(true)
            if (self.hour <= timeOther.endhour and self.hour >= timeOther.hour):
                if self.hour == timeOther.endhour:
                    if self.minute < timeOther.minute:
                        return True
                if self.hour == timeOther.hour:
                    if self.minute>timeOther.endminute:
                        return True
                return True
            if (self.endhour < timeOther.endhour and self.endhour > timeOther.hour):
                if self.endhour == timeOther.endhour:
                    if self.endminute < timeOther.minute:
                        return True
                if self.endhour == timeOther.hour:
                    if self.endminute > timeOther.endminute:
                        return True
                return True
        return False
