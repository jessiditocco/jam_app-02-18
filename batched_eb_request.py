"""Helper functions that server calls upon"""
# Import random
import random

# Requests library to talk to API
import requests
# To access our OS environment variables
import os

from flask import request
from model import db, connect_to_db, Event, Comment, User, BookmarkType, Bookmark, Search

# To use datetime module
from datetime import datetime
import json


EVENTBRITE_TOKEN = os.getenv('EVENTBRITE_TOKEN')
EVENTBRITE_URL = "https://www.eventbriteapi.com/v3/"


def get_batched_results(searches):
    """Gets batched api call results from EB api based on JAM users recent searches"""

    batched_search_list = []

    # Searches is a list of tuples in the form of (saerch term, search location)
    for search in searches:
        search_term = search[0]
        location = search[1]
        # This passes our search term and location in as a get request for each of the users searches
        eb_search = {"method":"GET", "relative_url": "events/search?q={}&location.address={}&categories=103".format(search_term, location)}

        batched_search_list.append(eb_search)

    # print batched_search_list

    headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

    # Jsonify the batched request dictionary and pass it to the post request in the payload
    batched_request = json.dumps(batched_search_list)

    # Pass the batched jsonified searches to the post request
    payload = {'batch': batched_request}

    # Will return only events with category ID that corresponds to music
    category_id = "103"

    
    response = requests.post(EVENTBRITE_URL + "batch/", headers=headers, 
        verify=True, params=payload)

   # Verifies SSL certificate
    verify = True

    batched_results = response.json()

    # Batched data will return data in the form of a list of each search result

    return batched_results


def get_list_of_suggested_events(batched_results, num_searches):
    """Returns a list of random events based on number of searches in batched search"""

    suggested_events = []

    # Our number of searches is 5 because we are grabbing 5 of the users most recent search terms
    for i in range(num_searches):

        # We want to turn the json for the results into a dictionary; one key for the dict is events
        events = json.loads(batched_results[i]["body"])
        list_of_events = events["events"]

        # Lets grab a random event for each search keyword and append to a list of recommended events
        suggested_events.append(random.choice(list_of_events))

    # print suggested_events
    # print len(suggested_events)

    return suggested_events

# suggested_events = get_list_of_suggested_events(get_batched_results(), 3)

def get_suggested_event_details(suggested_events):
    """Takes in a list of dicts of suggested events and returns details"""

    suggested_events_details = []
    

    for event in suggested_events:
        event_details = {}
        event_details["name"] = event["name"]["text"]
        event_details["id"] = event["id"]
        logo = event_details.get("logo", None)
        
        event_details["logo"] = event["logo"]["url"]
    
        suggested_events_details.append(event_details)

    return suggested_events_details


batched_results = get_batched_results([("techno", "San Francisco"), ("rock", "San Francisco"), ("hiphop", "San Francisco")])
list_suggested = get_list_of_suggested_events(batched_results, 3)
details = get_suggested_event_details(list_suggested)
