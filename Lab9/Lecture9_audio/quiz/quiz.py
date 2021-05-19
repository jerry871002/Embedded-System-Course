import RPi.GPIO as GPIO
import dht11
import time
import datetime

import speech_recognition as sr
from gtts import gTTS
import os

def generate_command():
    print('Generating command audio file...')
    tts = gTTS(text='please measure the temperature', lang='en')
    tts.save('measure.mp3')

    print('Converting mp3 into flac...')
    os.system('ffmpeg -i measure.mp3 measure.flac')

def recognize_command():
    r = sr.Recognizer()
    command = sr.AudioFile('measure.flac')
    with command as source:
        print("Use audio file as input!")
        audio = r.record(source)
    
    # recognize speech using Google Speech Recognition
    try:
        result = r.recognize_google(audio).split()
        print('Google Speech Recognition thinks the audio said:')
        print(result)
        return result
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand audio')
    except sr.RequestError as e:
        print(f'No response from Google Speech Recognition service: {e}')
    return None

def measure():
    # initialize GPIO
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BOARD)

    # read data using pin 
    instance = dht11.DHT11(pin=7)

    print('Measuring temperature...')
    while True:
        result = instance.read()
        if result.is_valid():
            GPIO.cleanup()
            return (result.temperature, result.humidity)

def result_audio(temp, humid):
    print('Generating result audio file...')
    tts = gTTS(text=f'the temperature is {temp} degree and the humidity is {humid} percent', lang='en')
    tts.save('result.mp3')

    os.system('omxplayer -o local -p result.mp3 > /dev/null 2>&1')

def main():
    generate_command()
    if 'measure' in recognize_command():
        temp, humid = measure()
        result_audio(temp, humid)

if __name__ == '__main__':
    main()
    