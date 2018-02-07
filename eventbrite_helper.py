"""Helper functions that server calls upon"""

# Requests library to talk to API
import requests
# To access our OS environment variables
import os
# # To use the datetime parser function from dateutil
from dateutil import parser
# To user the pytz library which converts timezones
import pytz



EVENTBRITE_TOKEN = os.getenv('EVENTBRITE_TOKEN')
EVENTBRITE_URL = "https://www.eventbriteapi.com/v3/"

def parse_datetime(timezone, local_dt_str):
    """Takes a timezone and local datetime string and returns date and time"""

    # This takes our local dateime string and parses the string and returns a DT object without TZ
    dt_obj = parser.parse(local_dt_str)

    # This returns a timezone object
    tz = pytz.timezone(timezone)

    # Makes a new datetime object with timezone
    local_time = tz.localize(dt_obj)

    local_time = local_time.ctime()

    return local_time


def get_events(search_term, location, start_date_kw):
    """Gets events from evenbrite API based on search keyword."""

    # To pass parameters through url you can use www.eventbriteapi.com/v3/events/search?variable=value&variable=value

    headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

    payload = {'q': search_term, 'location.address': location, 'start_date.keyword': start_date_kw}

    response = requests.get(EVENTBRITE_URL + "events/search/", headers=headers, verify=True, params=payload)

   # Verifies SSL certificate
    verify = True

    data = response.json()

    events = []

    # Loop through events and create a dict for each event which has event details
    for event in data["events"]:
        event_details = {}

        name = event["name"]["text"]
        event_id = event["id"]
        logo = event["logo"]

        # Get start/end local time and timezone to add to event details dict
        start_timezone = event["start"]["timezone"]
        start_time_local = event["start"]["local"]
        end_timezone = event["end"]["timezone"]
        end_time_local = event["end"]["local"]
        # Get start and end time in a parsed format
        start_time = parse_datetime(start_timezone, start_time_local)
        end_time = parse_datetime(end_timezone, end_time_local)
        # Add event details to the dictionary
        event_details["name"] = name
        event_details["event_id"] = event_id
        event_details["start_time"] = start_time
        event_details["end_time"] = end_time

        # Check to see if logo exits, if it doesn't, set it to a default image
        if logo is not None:
            logo = logo["original"]["url"]
            event_details["logo"] = logo
     
        else:
            event_details["logo"] = "https://upload.wikimedia.org/wikipedia/commons/6/69/Dog_morphological_variation.png"

        events.append(event_details)

    return events


def get_event_details(event_id):
    """Gets details about a specific event by id."""

    headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

    response = requests.get(EVENTBRITE_URL + "events/{}/".format(event_id), headers=headers, verify=True)

    event_details = response.json()

    return event_details
