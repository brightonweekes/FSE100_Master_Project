## Code for Buzzer and Ultrasonic=====================


import RPi.GPIO as GPIO
import time
from smbus2 import SMBus
from mlx90614 import MLX90614

TRIG = 17       # GPIO pin connected to Trig of Ultrasonic Sensor
ECHO = 18       # GPIO pin connected to Echo of Ultrasonic Sensor
BuzzerPin = 27  # GPIO pin connected to Buzzer
TempHolder = 0	# temporary Tempearature variable celsius
PainThresholdC = 43	# temperature when alert to hot pot


def setup():
    GPIO.setmode(GPIO.BCM)  # <-- Change BOARD to BCM
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(BuzzerPin, GPIO.OUT)
    GPIO.output(BuzzerPin, GPIO.HIGH)

def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        pass
    time1 = time.time()
    
    while GPIO.input(ECHO) == 1:
        pass
    time2 = time.time()

    duration = time2 - time1
    return (duration * 340 / 2) * 100  # Convert to centimeters

def buzzer_on():
    GPIO.output(BuzzerPin, GPIO.LOW)  # Turns the buzzer ON

def buzzer_off():
    GPIO.output(BuzzerPin, GPIO.HIGH)  # Turns the buzzer OFF

def beep(duration):
    buzzer_on()
    time.sleep(duration)
    buzzer_off()

def loop():
    while True:
        dis = distance()
        print(dis, 'cm')  # Print distance measurement

        threshold_crossed = False

        if TempHolder > PainThresholdC and threshold_crossed == False:  # If temperature exceeds threshold, buzz 
            threshold_crossed = True
            buzzer_on()
            time.sleep(0.5)  # Beep for 0.5 seconds
            buzzer_off()
        elif TempHolder < PainThresholdC and threshold_crossed == True:  # If temp lowers below threshold, reset the flag and beep twice
            threshold_crossed = False
            buzzer_on()
            time.sleep(0.1)
            buzzer_off()
            time.sleep(0.1)
            buzzer_on()
            time.sleep(0.1)
            buzzer_off()

        
        time.sleep(0.3)

def destroy():
    GPIO.cleanup()  # Reset GPIO settings


#+# End code for Buzzer and Ultrasonic====================


# Main loop code===========================

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

