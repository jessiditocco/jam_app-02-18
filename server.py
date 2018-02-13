"""Jams server"""
# Requests library to talk to API
import requests

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import db, connect_to_db, User, Event, Bookmark, BookmarkType, Comment

from eventbrite_helper import get_events, get_event_details, add_event_to_db, add_comment_to_db, remove_non_ascii


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

    # Gets all of the comments for the event; returns a list of comment objects
    comments = db.session.query(Comment).filter(Comment.event_id == event_id).all()

    print comments 

    return render_template("event_details.html", event_id=event_id, event_details=event_details, comments=comments)


@app.route('/add-bookmark', methods=["POST"])
def bookmark_event():
    """Adds event bookmark to user profile."""

    name = request.form.get("name")
    name = remove_non_ascii(name)

    bookmark_success = "Successfully bookmarked {}".format(name)

    bookmark_failure = "You must be logged in to bookmark and event."
    # Get event ID
    event_id = request.form.get("event_id")
    # Status of bookmark type "going", "interested"
    status = request.form.get("status")
    # Get user ID from session
    user_id = session.get("user_id")
    # Get the status: going or interested
    status = request.form.get("status")


    # If the user is logged in 
    if user_id:
        # Add the event that they pin to db
        add_event_to_db()
        # Make a bookmark in the bookmarks table

        # Get BookmarkType object out of DB based on status
        bookmark_type_object = db.session.query(BookmarkType).filter_by(bookmark_type=status).one()

        # Get the bookmark_type_id out of the db
        bookmark_type_id = bookmark_type_object.bookmark_type_id
        # Make a new Bookmark, passing it the user_id, event_id, and bookmarktype object
        # Add to DB
        bookmark = Bookmark(user_id=user_id, event_id=event_id, bookmark_type_id=bookmark_type_id)
        db.session.add(bookmark)
        db.session.commit()
        # Return success message as JSON to AJAX

        return bookmark_success

    else:
        return bookmark_failure

@app.route('/profile')
def display_profile():
    """Displays user's profile which has user's events by bookmark types."""

    user_id = session.get("user_id")

    user = User.query.filter_by(user_id=user_id).one()

    events_going = user.get_events("going")

    events_interested = user.get_events("interested")

    return render_template("profile.html", events_going=events_going, 
        events_interested=events_interested)


@app.route('/add_comment', methods=["POST"])
def post_comment():
    """Adds users comment to the database."""

    # Get userID from the session
    user_id = session.get("user_id")
    # Get eventID from the event details page
    event_id = request.form.get("event_id")
    # Get comment text from the payload
    comment = request.form.get("comment")

    # Get the current timestamp
    ## Not sure about this????

    # If the user is logged in, add the comment to the DB
    add_comment_to_db(user_id, event_id, comment)

    return comment


 

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