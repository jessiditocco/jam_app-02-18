"""Jams server"""
# Requests library to talk to API
import requests

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import db, connect_to_db, User, Event, Bookmark, BookmarkType, Comment, Search

from eventbrite_helper import (get_events, get_event_details, add_comment_to_db, create_user, add_bookmark_to_db, save_search_to_db, get_recent_searches)

from sendgrid_helper import send_email

import random

from batched_eb_request import (get_batched_results, get_list_of_suggested_events, 
get_suggested_event_details)


# When we create a Flask app, it needs to know what module to scan for things
# like routes so the __name__ is required
# this instantiates an object of the class flask
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variablei n Jinja2, it fails silently
# Fix this so that it raises an error instead
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage route"""

    return render_template("homepage.html")


@app.route('/get_recommendations.json')
def get_recommendations():
    """Gets recommended events for the user based on past searches"""

    ##### THIS USES BATCHED API REQUEST #####
    user_id = session.get("user_id")

    # If userID is None, return event reccomendations as none
    if not user_id:
        event_recommendation_details = None

        return jsonify(event_recommendation_details)

    # If the user is logged into the session, we want to check if they have searches
    if user_id:
        # This is a list of 5 search objects
        recent_searches = get_recent_searches(user_id)
        # If the user has recent searches, we want to do the batched api search
        if recent_searches:
            # Make a list of searches to call in our batched API request
            searches = []

            # Making a tuple for each search (searchterm, searchlocation) and append that to searches
            for search in recent_searches:
                searches.append(tuple([search.search_term, search.search_location]))
            print "SEARHCES", searches
            # Get batched results makes a batched request to EB api and returns json
            batched_results = get_batched_results(searches)

            # Returns a list of random events from batched_results; 1 random event for each search, should return 5
            suggested_events = get_list_of_suggested_events(batched_results, len(recent_searches))

            suggested_event_details = get_suggested_event_details(suggested_events)
    
            # Initialize a dictionary of all events
            # Loop through the list and add a key

            event_recommendation_details = {}
            num = 0
            for event_dict in suggested_event_details:
                event_recommendation_details["event{}".format(num)] = event_dict 
                num += 1

        # If there are no recent searches, return none for event recommendations
        else:
            event_recommendation_details = None

    return jsonify(event_recommendation_details)


@app.route('/register_new_user', methods=['POST'])
def register_proccess():
    """Proccess registration"""

    # Get variables from form
    name = request.form.get("name")
    email = request.form.get('email')
    password = request.form.get('password')

    # Query the DB and make sure that the user doesn't already exist
    user = db.session.query(User).filter((User.email == email) & (User.password == password)).first()
    # If user returns none, we want to create user
    if user == None:
        # Register new user and add user to DB, commit user
        new_user = create_user(name, email, password)
        # Once the user registers, add them to the session
        session["user_id"] = new_user.user_id
        result = {"message": "success"}
        return jsonify(result)

    else:
        result = {"message": "user was already in the DB"}
        return jsonify(result)


@app.route('/login', methods=['POST'])
def login_proccess():
    """Proccesses user and adds user to session."""

    # Get form variables
    email = request.form.get("email")
    password = request.form.get("password")

    # Check the DB to see if user exists and login matches
    user = db.session.query(User).filter((User.email == email) & (User.password == password)).first()
    print "This is the user!!!", user
    # If user is in DB, add user to the session
    # Flash success message
    # Return redirect to homepage
    if user:
        session["user_id"] = user.user_id
        result = {"message": "success"}
        print "session at user id!!!!", session["user_id"]
        return jsonify(result)
    else:
        result = {"message": "Wrong username/password combo"}
        return jsonify(result)


@app.route('/logout', methods=["GET"])
def logout():
    """Logs user out; removes user from session."""

    # Delete the user from the session
    del session["user_id"]
    # Redirect user back to homepage

    result = {"message": "success"}
    return jsonify(result)




@app.route('/show_events', methods=["POST"])
def show_events_by_keyword():
    """Returns html template with events by keyword."""

    search_term = request.form.get("event")
    location = request.form.get("location")
    start_date_kw = request.form.get("start_date_kw")

    user_id = session.get("user_id")
    # If the user is in the session, save the users' search to DB
    if user_id:
        save_search_to_db(user_id, search_term, location)
    # Get a list of events based on search term to pass to render events page
    events = get_events(search_term, location, start_date_kw)

    return render_template("events.html", events=events, search_term=search_term, location=location)


@app.route('/event_details')
def show_event_details():
    """Renders HTML template with information about a specific event"""

    event_id = request.args.get('event_id')

    print "THIS SHOULD BE EVENT ID GRABBED FROM HOMEPAGE", event_id

    event_details = get_event_details(event_id)

    user_id = session.get("user_id")
    # If the user_id exists in session, get the user object
    if user_id:
        # Gets all of the comments for the event; returns a list of comment objects
        # Only retrieve comments if user is logged in
        comments = db.session.query(Comment).filter(Comment.event_id == event_id).all()

        # Get the user object from user_id
        user_object = db.session.query(User).filter(User.user_id == user_id).one()
        # Get the user's name from the user object
        user_name = user_object.name
        # Gets bookmark for the event if the user has already bookmarked the event and is logged in
        # We want to display user's bookmarks if they have already bookmarked the event
        bookmark = db.session.query(Bookmark).filter((Bookmark.user_id == user_id) & (Bookmark.event_id == event_id)).first()

    else:
        user_name = "Not logged In."
        bookmark = None
        comments = None
        going_bookmarks = None

    # Get users going to the event
    event = db.session.query(Event).filter(Event.event_id == event_id).first()
    # If a user is logged in and the event exits in the database, we want to get all of the users going
    if user_id and event:
        users_going = event.get_attendees("going")
    else:
        users_going = None
       

    return render_template("event_details.html", event_id=event_id, 
    event_details=event_details, comments=comments, user_name=user_name, 
    bookmark=bookmark, users_going=users_going)



@app.route('/add_bookmark', methods=["POST"])
def bookmark_event():
    """Adds event bookmark to user profile."""

    name = request.form.get("name")
    # Get event ID
    event_id = request.form.get("event_id")
    # Status of bookmark type "going", "interested"
    status = request.form.get("status")
    # Get user ID from session
    user_id = session.get("user_id")
    # Get the status: going or interested
    status = request.form.get("status")

    # This helper function returns either bookmark_success or bookmark_failure message
    return add_bookmark_to_db(status, name, event_id, user_id)


@app.route('/profile')
def display_profile():
    """Displays user's profile which has user's events by bookmark types."""
    
    # Get the user_id from the profile/contact form
    user_id_from_form = request.args.get("user_id")

    # if there is a user_id from the profile/contact form, make that the user_id
    if user_id_from_form:
        user_id = user_id_from_form
    # If there isn't a user_id from the profile/contact form, user id from session
    else: 
        user_id = session.get("user_id")
        print "This is the user_id from session", user_id

    # Get the user object filtered by user_id 
    user = User.query.filter_by(user_id=user_id).one()
    # Returns a list of event objects that the user is going to
    events_going = user.get_events("going")
    # Returns a list of events that the user is interested in
    events_interested = user.get_events("interested")

    return render_template("profile.html", events_going=events_going, 
        events_interested=events_interested, user=user)


@app.route('/add_comment', methods=["POST"])
def post_comment():
    """Adds users comment to the database."""

    # Get userID from the session
    user_id = session.get("user_id")
    print "This is the user id!", user_id
    # Get the event id from data div
    event_id = request.form.get("event_id")
    print "This is the event_id!!!!!", event_id
    # Get comment text from the payload
    comment = request.form.get("comment")
    print "This is the comment!!!!!", comment
    # Add comment to DB
    add_comment_to_db(user_id, event_id, comment)
    # Get the user object from user_id so that i can add user name to comment
    user_object = db.session.query(User).filter(User.user_id == user_id).one()
    # Get the user's name from the user object
    user_name = user_object.name

    comment_details = {"comment": comment,
                "user_name": user_name}

    return jsonify(comment_details)

@app.route('/email', methods=["POST"])
def email_user():
    """Emails the user using sendgrid api"""

    # Get userID from the session
    # The user must be logged in bc can only see their profile if logged in
    user_id = session.get("user_id")
    # Get the current user from db
    current_user = db.session.query(User).filter(User.user_id == user_id).one()
    
    # Send_from will grab the users email from the current_user in the session
    send_from = current_user.email
    name = request.form.get("name")
    subject = request.form.get("subject")
    email_body = request.form.get("email_body")
    send_to = request.form.get("send_to")

    send_email(name, send_from, subject, email_body, send_to)

    success_message = "Your email has been sent."

    return success_message

@app.route('/map.json')
def get_map_details():
    """Gets event details for making our map"""

    # Get the user_id from the profile/contact form
    user_id_from_form = request.args.get("user_id")

    # if there is a user_id from the profile/contact form, make that the user_id
    if user_id_from_form:
        user_id = user_id_from_form
    # If there isn't a user_id from the profile/contact form, user id from session
    else: 
        user_id = session.get("user_id")
        print "This is the user_id from session", user_id

    # Get the user object filtered by user_id

    user = User.query.filter_by(user_id=user_id).one()

    # Get all of the events that the user is going to
    events_going = user.get_events("going")

    # Finding the average lat/long to pass through to center map around events
    sum_lat = 0
    sum_long = 0

    for event in events_going:
        sum_lat += event.latitude
        sum_long += event.longitude

    avg_lat = sum_lat / len(events_going)
    avg_long = sum_long / len(events_going)


    # Make a dictionary of nested dictionaries that contain info for each event the user is going to
    map_data = {"center": {"lat": avg_lat, "long": avg_long}}

    n = 0
    for event in events_going:
        map_details = {}
        map_details["address"] = event.address
        map_details["latitude"] = event.latitude
        map_details["longitude"] = event.longitude
        map_details["venue_name"] = event.venue_name
        map_details["name"] = event.name
        map_data["event{}".format(n)] = map_details
        n +=1

    print map_data

    return jsonify(map_data)

@app.route('/dom')
def show_example():

    return render_template("dom.html")






################################################################################
# listening for requests
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    # app.debug = True
    app.debug = True
    # Defeat the cache if debug mode true
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
