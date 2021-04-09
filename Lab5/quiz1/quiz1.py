from datetime import datetime, timedelta
import schedule
import time
import picamera

def take_pictures(nums):
    print('Start capturing…')
    with picamera.PiCamera() as camera:
        camera.start_preview()
        try:
            for i, filename in enumerate(camera.capture_continuous('image{counter:02d}.jpg')):
                print(filename)
                time.sleep(1)
                if i == nums - 1:
                    break
        finally:
            camera.stop_preview()
    return schedule.CancelJob

now = datetime.now()
print(f'Current time: {now}')
scheduled = now + timedelta(seconds=5)
print(f'Scheduled time: {scheduled}')

schedule.every().minute.at(f':{scheduled.second}').do(take_pictures, nums=5)

while True:
    schedule.run_pending()
    time.sleep(1)
