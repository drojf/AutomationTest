import busio
import adafruit_pcf8523
import time
import board

def rampLightOn():
    pass

def rampLightOff():
    pass

class Automation:
    def __init__(self, rtc):
        self.rtc = rtc

    def print_time(self):
        days = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")

        t = self.rtc.datetime
        #print(t)     # uncomment for debugging

        print("The date is %s %d/%d/%d" % (days[t.tm_wday], t.tm_mday, t.tm_mon, t.tm_year))
        print("The time is %d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec))

    def set_time(self, year, month, day, hour, minute, second, weekday):
        # yearday is not supported, isdst can be set but we don't do anything with it at this time
        t = time.struct_time((year, month, day, hour,  minute,  second, weekday, -1, -1)) # yday, isdst
        print("Setting time to:", t)     # uncomment for debugging
        rtc.datetime = t

    def check_actions(self):
        startHour = 9
        startMinute = 30
        startUnits = startHour * 60 + startMinute
        endHour = 11
        endMinute = 30
        endUnits = endHour * 60 + endMinute

        t = self.rtc.datetime
        currentUnit = t.tm_hour * 60 + t.tm_second

        if startUnits < endUnits:
            active = currentUnit > startUnits and currentUnit < endUnits
        else:
            # This case occurs when the action runs over midnight
            active = currentUnit > startUnits or currentUnit < endUnits #not (endUnits > currentUnit > startUnits)

        if not wasActive and active:
            startPeriodAction

        if wasActive and not active:
            endPeriodAction

