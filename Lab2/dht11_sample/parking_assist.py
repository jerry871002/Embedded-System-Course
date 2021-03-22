import RPi.GPIO as GPIO
import dht11
import time
import datetime

LED_PIN = 12
DHT_PIN = 16
TRIGGER_PIN = 18
ECHO_PIN = 22

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# read data using pin 
instance = dht11.DHT11(pin=DHT_PIN)

def measure():
    GPIO.output(TRIGGER_PIN, GPIO.HIGH)
    time.sleep(0.00001) # 10us
    GPIO.output(TRIGGER_PIN, GPIO.LOW)

    pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time.time()

    t = pulse_end - pulse_start

    # calculate sound speed using temperarure
    result = instance.read()
    if result.is_valid():
        v = 331.3 + 0.606 * result.temperature
    else:
        v = 343

    print(f'v = {v}')

    d = t * v / 2 # m
    return d * 100 # cm

def blink(delta):
    print("LED is on") 
    GPIO.output(LED_PIN, GPIO.HIGH) 
    time.sleep(delta)
    print("LED is off") 
    GPIO.output(LED_PIN, GPIO.LOW) 
    time.sleep(delta)

while True:
    d = measure()
    print(f"Distance: {d} cm")
    time.sleep(1)
    if d > 100:
        print("LED is off") 
        GPIO.output(LED_PIN, GPIO.LOW)
    elif 30 <= d <= 100:
        blink(0.5)
    elif d < 30:
        blink(0.2)
