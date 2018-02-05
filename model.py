"""Models and database functions for Jam project."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; were getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the "session" object, where we do most of our interactions

app = Flask(__name__)

DB_URI = "postgresql:///jams"

db = SQLAlchemy()

################################################################################
# Model definitions


class Users(db.Model):
    """User of jams website."""

    ___tablename___ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when user is printed."""

        return "<User ID={} email={} name={}".format(self.user_id, self.email, self.name)


class Events(db.Model):
    """Events on jams website."""

    ___tablename___ = "events"

    #### do i need event brite ID and event_id????
    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    eventbrite_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    address = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    url = db.Column(db.Integer(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        """Provide helpful representation when event is printed."""

        return "<Event ID={} Eventbrite ID={} Title={}".format(self.event_id, self.eventbrite_id, self.title)


class Bookmarks(db.Model):
    """User's bookmarks of specific events on jams website."""

    ___tablename___ = "bookmarks"

    bookmark_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event_id"), nullable=False)
    bookmark_type_id = db.Column(db.Integer, db.ForeignKey("bookmark_type_id"), nullable=False)

    def __repr__(self):
        """Provide helpful representation when a bookmark is printed."""

        return "<Bookmark ID={} User ID={} Event ID={} Bookmark Type ID={}".format(self.bookmark_id, self.user_id , self.event_id, self.bookmark_type_id)


class Bookmark_type(db.Model):
    """Types of bookmarks on jams website."""

    ___tablename___ = "bookmarks"

    bookmark__type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    

    def __repr__(self):
        """Provide helpful representation when a bookmark is printed."""

        return "<Bookmark ID={} User ID={} Event ID={} Bookmark Type ID={}".format(self.bookmark_id, self.user_id , self.event_id, self.bookmark_type_id)


################################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE URI'] = DB_URI

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

    db.create_all()


connect_to_db(app)
