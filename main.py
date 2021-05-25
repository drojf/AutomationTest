import busio
import adafruit_pcf8523
import time
import board
from library import Automation

def test():
    print("asdf")

if __name__ == '__main__':
    myI2C = busio.I2C(board.SCL, board.SDA)
    rtc = adafruit_pcf8523.PCF8523(myI2C)
    automation = Automation(rtc)

    while True:
        automation.print_time()
        time.sleep(1) # wait a second