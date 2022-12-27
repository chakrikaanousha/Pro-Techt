import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)

while True:
    i = GPIO.input(11)
    if i == 0:
        print("No intruders")
        time.sleep(1)
    elif i == 1:
        print("Intruder Alert!")
        time.sleep(1)