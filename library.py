import busio
import adafruit_pcf8523
import time
import board
import pwmio
import neopixel

class LEDDriver:
    def __init__(self, led):
        self.led = led
        self.led.brightness = 1.0

    def rampLightOn(self):
        self.led[0] = (255, 255, 255)

    def rampLightOff(self):
        self.led[0] = (0, 0, 0)


class Automation:
    def __init__(self, rtc, led):
        self.rtc = rtc # type: adafruit_pcf8523.PCF8523
        self.led = led # type: LEDDriver
        self.wasActive = False

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
        self.rtc.datetime = t

    def check_actions(self):
        startHour = 23
        startMinute = 00
        startUnits = startHour * 60 + startMinute
        endHour = 23
        endMinute = 1
        endUnits = endHour * 60 + endMinute

        t = self.rtc.datetime
        currentUnit = t.tm_hour * 60 + t.tm_min

        # Current logic will turn on as soon as the hour/minute match start time (at the start of the minute)
        # And will turn off as soon as hour/minute match end time (at the start of the minute)
        if startUnits < endUnits:
            active = currentUnit >= startUnits and currentUnit < endUnits
        else:
            # This case occurs when the action runs over midnight
            active = currentUnit >= startUnits or currentUnit < endUnits #not (endUnits > currentUnit > startUnits)

        print("StartUnit %s EndUnit %s CurrentUnit %s Active %s" % (startUnits, endUnits, currentUnit, active))

        if not self.wasActive and active:
            print("Turning lights on")
            self.led.rampLightOn()

        if self.wasActive and not active:
            print("Turning lights off")
            self.led.rampLightOff()

        self.wasActive = active

def getAutomation():
    myI2C = busio.I2C(board.SCL, board.SDA)
    rtc = adafruit_pcf8523.PCF8523(myI2C)
    led = neopixel.NeoPixel(board.NEOPIXEL, 1)
    ledDriver = LEDDriver(led)
    automation = Automation(rtc, ledDriver)
    return automation
