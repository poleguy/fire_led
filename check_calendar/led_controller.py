# to set up:
# share calendar from outlook.office.com
# get email from there, extract ics link.
# this script will then parse that ics link and tell you either not busy, almost busy, or busy.
#
# https://stackoverflow.com/questions/3408097/parsing-files-ics-icalendar-using-python


#from icalevents.icalevents import events

import check_calendar
import bash
import time
from urllib.error import HTTPError

def main():

    state = 'unknown'
    while True:

        print("checking status")
        try:
            status = check_calendar.main()
        except HTTPError:
            # make it flash to notice how often this happens
            status = {'calendar_status' : "error"}
            continue
    


        if status['calendar_status'] == state:
            print(f'nothing to do: {state}')
        elif status['calendar_status'] == 'error':
            cmd = "rsync -P /home/poleguy/flippy-data/2022/fire_led/red_stripes.jpg pi@fire.local:/run/user/1000/image.jpg"
        elif status['calendar_status'] == 'busy':
            cmd = "rsync -P /home/poleguy/flippy-data/2022/fire_led/busy.jpg pi@fire.local:/run/user/1000/image.jpg"
        elif status['calendar_status'] == 'pre meeting':
            cmd = "rsync -P /home/poleguy/flippy-data/2022/fire_led/pre_meeting.jpg pi@fire.local:/run/user/1000/image.jpg"
        else:
            #cmd = "rsync -P /home/poleguy/flippy-data/2022/fire_led/idle.jpg pi@fire.local:/home/pi/fire_led/image.jpg"
            cmd = "rsync -P /home/poleguy/flippy-data/2022/fire_led/purple_glow.jpg pi@fire.local:/run/user/1000/image.jpg"

        state = status['calendar_status']

        try:
            bash.bash(cmd)
            # feed watchdog to prevent leds from going to idle state
            bash.bash("ssh pi@fire.local touch /run/user/1000/dog_food")

        except ValueError as e:
            if "Bash command failed" in str(e):
                # e.g. ssh: Could not resolve hostname fire.local: Name or service not known
                # keep trying until it comes back
                continue
            raise

        time.sleep(30)
            
if __name__ == '__main__':
    import typer
    typer.run(main)


