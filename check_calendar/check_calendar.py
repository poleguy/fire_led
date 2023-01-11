# to set up:
# share calendar from outlook.office.com
# get email from there, extract ics link.
# this script will then parse that ics link and tell you either not busy, almost busy, or busy.
#
# https://stackoverflow.com/questions/3408097/parsing-files-ics-icalendar-using-python


#from icalevents.icalevents import events

import json
#import requests
import urllib.request

#import wget
#import vobject
#from ics import Calendar, Event
#import ics
#from tzlocal import get_localzone
from icalendar import Calendar

# https://icalevents.readthedocs.io/en/latest/
#from icalevents.icalevents import events_async, latest_events, all_done
from time import sleep
import icalendar
import recurring_ical_events


import pytz
import datetime
import os

def main(url_file = "calendar_url.txt"):

    # put the url to the ics in the "secret" (not in github) url file
    with open(url_file, 'r') as f:
        url = f.read()

    filename = "reachcalendar.ics"

    if os.path.exists(filename):
        os.remove(filename)
    
    #wget.download(url) # this hung on me.. punting
    
    # https://stackoverflow.com/questions/35115513/python-bad-request-in-get-but-wget-and-curl-work
    #headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    # https://stackoverflow.com/questions/12624133/wget-with-python-time-limit
    
    # https://stackoverflow.com/questions/20227324/programmatically-download-content-from-shared-dropbox-folder-links
#    headers = {  'User-Agent': 'Wget/1.20.3 (linux-gnu)',
#                 'Accept': '*/*',
#                 'Accept-Encoding': 'identity',
#                 'Host': 'outlook.office365.com',
#                 'Connection': 'Keep-Alive'}
#
#    print(url)
#    response = requests.get(url, timeout=10.0, data=json.dumps(headers=headers)



    response = urllib.request.urlopen(url, timeout=10.0)
    data = response.read()      # a `bytes` object
    #text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
    
    with open(filename, 'wb') as f:
        f.write(data)


    
    
    #utc=pytz.UTC
    # https://stackoverflow.com/questions/31304890/wrong-aware-datetime-with-pytz-and-america-chicago
    #chicago = pytz.timezone('America/Chicago')
    chicago_time = pytz.timezone("America/Chicago")


    def pre_meeting():
    #
        start =  datetime.datetime.now() 
        start = chicago_time.localize(start)
    
        end = datetime.datetime.now()
        end = chicago_time.localize(end)
        end = end + datetime.timedelta(minutes=2)
    
        with open(filename, 'r') as f:
            ical_string = f.read()
    
        start_date = start
        end_date = end
    
        print(start_date)
        print(end_date)
        
        calendar = icalendar.Calendar.from_ical(ical_string)
        events = recurring_ical_events.of(calendar).between(start_date, end_date)
        found_meeting = False
        for event in events:
            start = event["DTSTART"].dt
            duration = event["DTEND"].dt - event["DTSTART"].dt
            transp = event["TRANSP"]
            print(f"start {start} duration {duration} transp {transp}")
            if transp == "OPAQUE":
                found_meeting = True
        return found_meeting

    def busy():
    #
        start =  datetime.datetime.now() 
        start = chicago_time.localize(start)
    
        end = datetime.datetime.now()
        end = chicago_time.localize(end)
    
        with open(filename, 'r') as file:
            ical_string = file.read()
    
        start_date = start
        end_date = end
    
        print(start_date)
        print(end_date)
        
        calendar = icalendar.Calendar.from_ical(ical_string)
        events = recurring_ical_events.of(calendar).between(start_date, end_date)
        found_meeting = False
        for event in events:            
            start = event["DTSTART"].dt
            duration = event["DTEND"].dt - event["DTSTART"].dt
            transp = event["TRANSP"]
            print(f"start {start} duration {duration} transp {transp}")
            if transp == "OPAQUE":
                found_meeting = True
        return found_meeting

    if busy():
        data = {"calendar_status":"busy"}
    else:
        if pre_meeting():
            data = {"calendar_status":"pre meeting"}
        else:
            data = {"calendar_status":"free"}

    print(data)
    # https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
    with open('calendar_status.json', 'w') as f:
        json.dump(data, f)

    return data
        

def _format_name(address):
    """Retrieve the e-mail and the name from an address.
    :arg an address object, e.g. mailto:test@test.test
    :returns str: The name and the e-mail address.
    """
    email = address.split(':')[-1]
    name = email.split('@')[0]
    if not email:
        return ''
    return f"{name} <{email}>"


def _format_attendees(attendees):
    """Format the list of attendees.
    :arg any attendees: Either a list, a string or a vCalAddress object.
    :returns str: Formatted list of attendees.
    """
    if isinstance(attendees, list):
        return '\n'.join(map(lambda s: s.rjust(len(s) + 5), map(_format_name, attendees)))
    return _format_name(attendees)

            
def view(event):
    """Make a human readable summary of an iCalendar file.
    :returns str: Human readable summary.
    """
    summary = event.get('summary', default='')
    organizer = _format_name(event.get('organizer', default=''))
    attendees = _format_attendees(event.get('attendee', default=[]))
    location = event.get('location', default='')
    comment = event.get('comment', '')
    description = event.get('description', '').split('\n')
    description = '\n'.join(map(lambda s: s.rjust(len(s) + 5), description))

    start = event.decoded('dtstart')
    if 'duration' in event:
        end = event.decoded('dtend', default=start + event.decoded('duration'))
    else:
        end = event.decoded('dtend', default=start)
    duration = event.decoded('duration', default=end - start)
    if isinstance(start, datetime.datetime):
        start = start.astimezone(start.tzinfo)
    start = start.strftime('%c')
    if isinstance(end, datetime.datetime):
        end = end.astimezone(end.tzinfo)
    end = end.strftime('%c')

    

    return f"""    Status: {flag}
    Organizer: {organizer}
    Attendees:
{attendees}
    Summary    : {summary}
    Starts     : {start}
    End        : {end}
    Duration   : {duration}
    Location   : {location}
    Comment    : {comment}
    Description:
{description}"""





      
            
if __name__ == '__main__':
    import typer
    typer.run(main)


