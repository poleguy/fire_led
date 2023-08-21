to copy to raspberry pi:
from fire_led directory:

rsync -rahP ./ pi@fire.local:/home/pi/fire_led/ --exclude cenv

to run on pi:

#add to rc.local and boot

or run:

sudo python fire_led.py

or test on pc with:

python fire_led.py --mock

or the older:

python test_mock_neopixel.py


https://practicalgit.com/blog/make-git-ignore-local-changes-to-tracked-files.html

    git update-index --assume-unchanged check_calendar/reachcalendar.ics
    git update-index --assume-unchanged check_calendar/calendar_status.json


# setup

on pi, run: 

bash setup.sh
cp led.service /lib/systemd/system/led.service

on pc:

add led_controller.service

to stop:

'''
  sudo systecmctl stop led_controller.service
  sudo systecmctl disable led_controller.service
'''


# troubleshooting

RuntimeError: NeoPixel support requires running with sudo, please try again!

use sudo

PermissionError: [Errno 13] Permission denied: '/run/shm/debug.log'

rm /run/shm/debug.log 
