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
import urllib.error
import socket

#import requests.exceptions


# https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time
if __package__ is None or __package__ == '':
    # uses current directory visibility
    import logger
else:
    # uses current package visibility
    from . import logger


logger = logger.get_logger(__name__)

def main():
    logger.debug("Starting up")

    state = 'unknown'
    while True:

        print("checking status")
        # https://stackoverflow.com/questions/8763451/how-to-handle-urllibs-timeout-in-python-3
        try:
            status = check_calendar.main()
#        except requests.exceptions.Timeout:
#            logger.debug("Timeout")
#            # make it flash to notice how often this happens
#            status = {'calendar_status' : "error"}
#            continue
#        except requests.exceptions.ConnectionError:
#            logger.debug("Connection Error")
#            # make it flash to notice how often this happens
#            status = {'calendar_status' : "error"}
#            continue
        except urllib.error.HTTPError as e:
            logger.debug("HTTP Error")
            # make it flash to notice how often this happens
            status = {'calendar_status' : "error"}
            continue
        except urllib.error.URLError as e:
            logger.debug("URL Error")
            logger.debug(type(e))
            # make it flash to notice how often this happens
            status = {'calendar_status' : "error"}
            continue
        # https://stackoverflow.com/questions/8763451/how-to-handle-urllibs-timeout-in-python-3
        except socket.timeout as e:
            logger.debug("Timeout Error")
            logger.debug(type(e))
            # make it flash to notice how often this happens
            status = {'calendar_status' : "error"}
            continue
           
    


        if status['calendar_status'] == state:
            print(f'nothing to do: {state}')
        elif status['calendar_status'] == 'error':
            cmd = "rsync -P /home/poleguy/flippy-data/2023/fire_led/red_stripes.jpg pi@fire.local:/run/shm/image.jpg"
        elif status['calendar_status'] == 'busy':
            cmd = "rsync -P /home/poleguy/flippy-data/2023/fire_led/busy.jpg pi@fire.local:/run/shm/image.jpg"
        elif status['calendar_status'] == 'pre meeting':
            cmd = "rsync -P /home/poleguy/flippy-data/2023/fire_led/pre_meeting.jpg pi@fire.local:/run/shm/image.jpg"
        else:
            #cmd = "rsync -P /home/poleguy/flippy-data/2023/fire_led/idle.jpg pi@fire.local:/home/pi/fire_led/image.jpg"
            cmd = "rsync -P /home/poleguy/flippy-data/2023/fire_led/purple_glow.jpg pi@fire.local:/run/shm/image.jpg"

        state = status['calendar_status']

        try:
            bash.bash(cmd)
            # feed watchdog to prevent leds from going to idle state
            bash.bash("ssh pi@fire.local touch /run/shm/dog_food")

        except ValueError as e:
            if "Bash command failed" in str(e):
                # e.g. ssh: Could not resolve hostname fire.local: Name or service not known
                # keep trying until it comes back
                logger.debug("Bash command failed")
                continue
            raise

        time.sleep(30)
            
if __name__ == '__main__':
    import typer
    typer.run(main)


