to copy to raspberry pi:
rsync -rahP ./ pi@fire.local:/home/pi/fire_led/

to run
add to rc.local and boot
or run 
python test_mock_neopixel.py

https://practicalgit.com/blog/make-git-ignore-local-changes-to-tracked-files.html

    git update-index --assume-unchanged check_calendar/reachcalendar.ics
    git update-index --assume-unchanged check_calendar/calendar_status.json


# setup
add led_controller.service
to stop:

'''
  sudo systecmctl stop led_controller.service
  sudo systecmctl disable led_controller.service
'''
