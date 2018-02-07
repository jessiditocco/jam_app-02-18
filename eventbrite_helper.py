"""Helper functions that server calls upon"""

# Requests library to talk to API
import requests
# To access our OS environment variables
import os

EVENTBRITE_TOKEN = os.getenv('EVENTBRITE_TOKEN')
EVENTBRITE_URL = "https://www.eventbriteapi.com/v3/"


def get_events(search_term):
    """Gets events from evenbrite API based on search keyword."""

    # To pass parameters through url you can use www.eventbriteapi.com/v3/events/search?variable=value&variable=value

    # search_term = request.form.get("event")

    # r = requests.get('https://www.eventbriteapi.com/v3/events/search/?token=K24Y3YW4SN66CIIPMPNG&q={}'.format(search_term))

    # print r.json()

    # return redirect('/')

    headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

    payload = {'q': search_term}

    response = requests.get(EVENTBRITE_URL + "events/search/", headers=headers, verify=True, params=payload)

    data = response.json()

    events = []

    for event in data["events"]:
        event_details = {}

        name = event["name"]["text"]
        event_id = event["id"]
        # logo = event["logo"]["original"]["url"]

        event_details["name"] = name
        event_details["event_id"] = event_id

        ######### figure out logo stuff
        # if logo is not None:
        #     event_details["logo"] = logo
     
        # else:
        #     event_details["logo"] = "No Event Logo"

        events.append(event_details)

    return events

def get_details(event_id):
    """Gets details about a specific event by id."""

    headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

    response = requests.get(EVENTBRITE_URL + "events/event_id/", headers=headers, verify=True)

    data = response.json()


    return data
