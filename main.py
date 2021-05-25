import busio
import adafruit_pcf8523
import time
import board
import library
from library import Automation, LEDDriver

def test():
    print("asdf")

if __name__ == '__main__':
    automation = library.getAutomation()

    while True:
        automation.print_time()
        automation.check_actions()
        time.sleep(1) # wait a second
