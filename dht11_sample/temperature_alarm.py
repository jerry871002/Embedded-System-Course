import RPi.GPIO as GPIO 
import dht11
import time
import datetime

LED_PIN = 12
DHT_PIN = 16

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(LED_PIN, GPIO.OUT)

# read data using pin 
instance = dht11.DHT11(pin=DHT_PIN)

try:
    while True:
        result = instance.read()
        print(f"Temperature: {result.temperature}")
        if result.is_valid() and result.temperature >= 20:
            print("LED is on") 
            GPIO.output(LED_PIN, GPIO.HIGH)
        else:
            print("LED is off") 
            GPIO.output(LED_PIN, GPIO.LOW) 
        time.sleep(2)

except KeyboardInterrupt:
    print("Cleanup")

finally:
    GPIO.output(LED_PIN, GPIO.LOW) 
    GPIO.cleanup()
