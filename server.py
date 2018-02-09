"""Jams server"""
# Requests library to talk to API
import requests

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import db, connect_to_db, User, Event, Bookmark, BookmarkType, Comment

from eventbrite_helper import get_events
from eventbrite_helper import get_event_details


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


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("registration_form.html")


@app.route('/register', methods=['POST'])
def register_proccess():
    """Proccess registration"""

    # Get variables from form
    name = request.form.get("name")
    email = request.form.get('email')
    password = request.form.get('password')

    # Register new user and add user to DB, commit user
    new_user = User(email=email, name=name, password=password)
    db.session.add(new_user)
    db.session.commit()

    # Flash a message saying that the user has successfully registered
    flash("User {} successfully added".format(name))

    return redirect('/')


@app.route('/login', methods=['GET'])
def login_form():
    """Shows login form."""

    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_proccess():
    """Proccesses user and adds user to session."""
    #### IS THIS THE BEST WAY TO CHECK LOGIN?

    # Get form variables
    email = request.form.get("email")
    password = request.form.get("password")

    # Check the DB to see if user exists and login matches
    user = db.session.query(User).filter((User.email == email) & (User.password == password)).first()

    # If user is in DB, add user to the session
    # Flash success message
    # Return redirect to homepage
    if user:
        session["user_id"] = user.user_id
        flash("User successfully logged in")
        return redirect('/')
    # If user is not in session, redirect to login page
    else:
        flash("Email/password combination doesn't exist. Try again")
        return redirect('/login')


@app.route('/logout', methods=["GET"])
def logout():
    """Logs user out; removes user from session."""

    print session
    del session["user_id"]
    print session
    flash("User has been successfully logged out")
    return redirect("/")



@app.route('/show_events', methods=["POST"])
def show_events_by_keyword():
    """Returns html template with events by keyword."""

    search_term = request.form.get("event")
    location = request.form.get("location")
    start_date_kw = request.form.get("start_date_kw")

    events = get_events(search_term, location, start_date_kw)

    return render_template("events.html", events=events, search_term=search_term)



@app.route('/event_details')
def show_event_details():
    """Renders HTML template with information about a specific event"""

    event_id = request.args.get('event_id')

    event_details = get_event_details(event_id)

    print event_details

    return render_template("event_details.html", event_id=event_id, event_details=event_details)


@app.route('/add-bookmark', methods=["POST"])
def bookmark_event():
    """Adds event bookmark to user profile."""

    event_added = "Logged in & added event"
    not_logged = "Not logged in; no event added"

    user_id = session.get("user_id")

    if user_id:

        event_id = request.form.get("event_id")
        status = request.form.get("status")
        name = request.form.get("name")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        address = request.form.get("address")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        eb_url = request.form.get("eb_url")
        description = request.form.get("description")
        venue_name = request.form.get("venue_name")
        logo = request.form.get("logo")
        
        # Get event by event id
        event = Event.query.get(event_id)
        # if that event doesn't exist in the table: add it
        if event == None:
            # Add event to table
            event = Event(event_id=event_id, name=name, start_time=start_time, 
            end_time=end_time, address=address, latitude=latitude, longitude=longitude, venue_name=venue_name, logo=logo)

            db.session.add(event)
            db.session.commit()

        return event_added

    else:
        flash("You cannot bookmark an event without being logged in; please login")
        return not_logged


 

################################################################################
# listening for requests
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    # app.debug = True
    app.debug = True
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")