"""Jams server"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import db, connect_to_db, User, Event, Bookmark, BookmarkType, Comment

import requests
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
    flash("User {} successfully added".format(email))

    return redirect('/')

@app.route('/show_events', methods=["POST"])
def show_events_by_keyword():

    search_term = request.form.get("event")
    print "!!!!!!!!!!!!!!!!!", search_term
    

    r = requests.get('https://www.eventbriteapi.com/v3/events/search/?token=K24Y3YW4SN66CIIPMPNG&q={}'.format(search_term))

    print r.json()


    return redirect('/')


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