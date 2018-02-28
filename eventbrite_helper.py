"""Helper functions that server calls upon"""

# Requests library to talk to API
import requests
# To access our OS environment variables
import os
# # To use the datetime parser function from dateutil
from dateutil import parser
# To user the pytz library which converts timezones
import pytz
from flask import request
from model import db, connect_to_db, Event, Comment, User, BookmarkType, Bookmark, Search

# To use datetime module
from datetime import datetime


EVENTBRITE_TOKEN = os.getenv('EVENTBRITE_TOKEN')
EVENTBRITE_URL = "https://www.eventbriteapi.com/v3/"


def create_user(name, email, password):
    """Creates a new user in the DB."""

    new_user = User(email=email, name=name, password=password)
    db.session.add(new_user)
    db.session.commit()


def parse_datetime(timezone, local_dt_str):
    """Takes a timezone and local datetime string and returns date and time"""

    # This takes our local dateime string and parses the string and returns a DT object without TZ
    dt_obj = parser.parse(local_dt_str)

    # This returns a timezone object
    tz = pytz.timezone(timezone)

    # Makes a new datetime object with timezone
    local_time = tz.localize(dt_obj)

    # local_time = local_time.ctime()

    local_time = local_time.strftime('%A, %B %-d at %-I:%M%p')

    return local_time


def get_venue_details(venue_id):
    """Gets information about a venue based on the venue id."""

    headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

    response = requests.get(EVENTBRITE_URL + "venues/{}/".format(venue_id), 
        headers=headers, verify=True)

    data = response.json()

    # Get fields back from the JSON response
    name = data["name"]
    address = data["address"]["address_1"]
    city = data["address"]["city"]
    region = data["address"]["region"]
    latitude = data["address"]["latitude"]
    longitude = data["address"]["longitude"]
    full_address = data["address"]["localized_address_display"]

    venue_details = {"name": name, "address": address, 'full_address': full_address, 
    "city": city, "region": region, "latitude": latitude, "longitude":longitude}

    return venue_details


def get_events(search_term, location, start_date_kw):
    """Gets events from evenbrite API based on search keyword."""

    # To pass parameters through url you can use www.eventbriteapi.com/v3/events/search?variable=value&variable=value

    headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

    # Will return only events with category ID that corresponds to music
    category_id = "103"

    payload = {'q': search_term, 'location.address': location, 
    'start_date.keyword': start_date_kw, 'categories': category_id}

    response = requests.get(EVENTBRITE_URL + "events/search/", headers=headers, 
        verify=True, params=payload)

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
    # Returns a list of dictionaries for each event with event details
    return events


def get_event_details(event_id):
    """Gets details about a specific event by id."""

    headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

    response = requests.get(EVENTBRITE_URL + "events/{}/".format(event_id), headers=headers, verify=True)

    data = response.json()
    # Get fields back from json response

    name = data['name']['text']
    description = data['description']['text']
    eb_url = data['url']
    # We will return the nicely formated start and end times
    start_time = parse_datetime(data['start']['timezone'], data['start']['local'])
    end_time = parse_datetime(data['end']['timezone'], data['end']['local'])
    # We will pass timezone and local times to the front end so we can seed our events database with correct datetime format
    start_time_tz = data['start']['timezone']
    start_time_local = data['start']['local']
    end_time_tz = data['end']['timezone']
    end_time_local = data['end']['local']

    venue_id = data['venue_id']
    logo = data['logo']


    # Get details about a venue by id
    venue_details = get_venue_details(venue_id)

    address = venue_details["full_address"]
    venue_name = venue_details["name"]
    longitude = venue_details["longitude"]
    latitude = venue_details["latitude"]

    # Checks logo for url
    if logo is not None:
        logo = logo["original"]["url"]
    
    else:
        logo = "http://www.wellesleysocietyofartists.org/wp-content/uploads/2015/11/image-not-found.jpg"
    
    # Create event details dictionary to pass through to Jinja
    event_details = {'event_id': event_id, 'name': name, 'description': description, 
    'eb_url': eb_url, 'start_time': start_time, 'end_time': end_time, 'venue_id': venue_id, 
    'logo': logo, 'venue_name': venue_name, 'address': address, 'longitude': longitude, 
    'latitude': latitude, 'address': address, 'start_time_tz': start_time_tz,
    'start_time_local': start_time_local, 'end_time_tz': end_time_tz, 
    'end_time_local': end_time_local}

    return event_details


def add_event_to_db():
    """Adds an event to the database if a user bookmarks the event as going or interested."""

    event_id = request.form.get("event_id").strip()

    # Get event by event id
    event = Event.query.get(event_id)
    # if that event doesn't exist in the table: add it to the table
    if event:
        return

    status = request.form.get("status").strip()
    name = request.form.get("name").strip()
    # Start end end time in a nice format
    start_time = request.form.get("start_time").strip()
    end_time = request.form.get("end_time").strip()
    address = request.form.get("address").strip()
    latitude = request.form.get("latitude").strip()
    longitude = request.form.get("longitude").strip()

    # Since we are getting URL from form, we are getting entire element
    # We must split the URL to get only the link
    eb_url = request.form.get("eb_url").strip()
    eb_url = eb_url.split("\"")
    eb_url = eb_url[1]

    description = request.form.get("description").strip()
    venue_name = request.form.get("venue_name").strip()
    # This gets just the image url back from logo div
    logo = request.form.get("logo").strip()

    # This gets our timezone back in the datetime format
    start_time_tz = request.form.get("start_time_tz")
    start_time_local = request.form.get("start_time_local")
    end_time_tz = request.form.get("end_time_tz")
    end_time_local = request.form.get("end_time_local")

    # Add event to table
    event = Event(event_id=event_id, name=name, start_time=start_time, 
    end_time=end_time, address=address, latitude=latitude, 
    longitude=longitude, venue_name=venue_name, logo=logo, 
    start_time_tz=start_time_tz, start_time_local=start_time_local, 
    end_time_tz=end_time_tz, end_time_local=end_time_local, eb_url=eb_url)

    db.session.add(event)
    db.session.commit()

   


def add_comment_to_db(user_id, event_id, comment):
    """Adds a comment to the database if the user is logged in."""

    # Add comment to the comments table
    comment = Comment(user_id=user_id, event_id=event_id, comment=comment)

    db.session.add(comment)
    db.session.commit()


def remove_non_ascii(text):
    """Removes non ascii charecters from string."""

    return ''.join(i for i in text if ord(i)<128)


def add_bookmark_to_db(status, name, event_id, user_id):
    """Adds bookmark to DB or updates bookmark type if bookmark already exists"""

    bookmark_success = "Successfully bookmarked {} as {}".format(name, status)
    bookmark_failure = "You must be logged in to bookmark and event."
    # Removes non_ascii charecters from event names
    name = remove_non_ascii(name)


    # If the user is logged in
    if user_id:
        # Add the event that they pin to db only if the event doesn't already exist
        add_event_to_db()

        # Get BookmarkType object out of DB based on status
        bookmark_type_object = db.session.query(BookmarkType).filter_by(bookmark_type=status).one()

        print "1", bookmark_type_object, type(bookmark_type_object)

        # Get the bookmark_type_id out of the db, 1 for going, 2 for interested: gives us an int
        bookmark_type_id = bookmark_type_object.bookmark_type_id

        print "2", bookmark_type_object, type(bookmark_type_id)

        # Before make bookmark, check whether it exists; if it doesn't, create it, if it does, update it w bookmark type
        # We use .first() instead of .one() because with .one() if there are none, we get error
        # With .first() none gets returned if there isn't a bookmark
        bookmark_for_event = db.session.query(Bookmark).filter((Bookmark.event_id == event_id) & (Bookmark.user_id == user_id)).first()
        print "3", bookmark_for_event, type(bookmark_for_event)

        # If bookmark for event doesn't already exist, we want to create the bookmark
        if bookmark_for_event == None:
            # Make a new Bookmark, passing it the user_id, event_id, and bookmarktype object, add & commit
            bookmark = Bookmark(user_id=user_id, event_id=event_id, bookmark_type_id=bookmark_type_id)
            print "If event doesn't exists, we make bookmark", bookmark
            db.session.add(bookmark)
            db.session.commit()
            # Return success message
            return bookmark_success
        # If the bookmark for event already exist, we want to update the bookmark type
        else:
            bookmark_for_event.bookmark_type_id = bookmark_type_id
            print "If event does exist, we want to update the status", bookmark_for_event
            db.session.commit()
            return bookmark_success

    # If the user is not logged in, return please login message
    else:
        return bookmark_failure

def save_search_to_db(user_id, search_term, location):
    """Saves searches to DB based on user_id."""

    timestamp = datetime.now()

    new_search = Search(user_id=user_id, timestamp=timestamp, search_term=search_term, search_location=location)

    db.session.add(new_search)
    db.session.commit()

def get_recent_searches(user_id):
    """Gets a list of recent searches based on user_id."""

    current_user = User.query.filter(User.user_id == user_id).one()

    recent_searches = current_user.get_recent_searches()

    print "here are all of the recent searchs!!!", recent_searches

    return recent_searches

