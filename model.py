"""Models and database functions for Jam project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; were getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the "session" object, where we do most of our interactions

# app = Flask(__name__)

DB_URI = "postgresql:///jams"

db = SQLAlchemy()

################################################################################
# Model definitions, creating ORM


class User(db.Model):
    """Users of jams website."""

    #tablename has two underscores
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when user is printed."""

        return "<User ID={} email={} name={}".format(self.user_id, self.email, self.name)

    # makes relationship between users and events based on bookmark type
    def get_events(self, status):
        """Gets a list of events for a particular user based on bookmark type."""

        type_id = (BookmarkType.query
                                .filter(BookmarkType.bookmark_type == status)
                                .one().bookmark_type_id)

        return (Event.query.join(Bookmark)
                            .filter(Bookmark.bookmark_type_id == type_id,
                                    Bookmark.user_id == self.user_id,
                                    Event.event_id == Bookmark.event_id).all())


class Event(db.Model):
    """Events on jams website."""

    __tablename__ = "events"

    # Made desc, logo, and eb_url nullable for testing purposes

    event_id = db.Column(db.String(200), autoincrement=False, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    # This is start and end time formated nicely
    start_time = db.Column(db.String(100), nullable=False)
    end_time = db.Column(db.String(100), nullable=False)
    # This is start and end time in datetime format
    start_time_tz = db.Column(db.String(200), nullable=True)
    start_time_local = db.Column(db.DateTime, nullable=True)
    end_time_tz = db.Column(db.String(200), nullable=True)
    end_time_local = db.Column(db.DateTime, nullable=True)

    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.String(100), nullable=False)
    longitude = db.Column(db.String(100), nullable=False)
    eb_url = db.Column(db.String(300), nullable=True)
    description = db.Column(db.Text, nullable=True)
    venue_name = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String(200), nullable=True)


    def __repr__(self):
        """Provide helpful representation when event is printed."""

        return "<Event ID={} Name={}".format(self.event_id, self.name)

    # Makes relationship between events and users based on bookmark types
    def get_attendees(self, status):
        """Returns all users for a specific event based on type of bookmark."""

        type_id = (BookmarkType.query
                            .filter(BookmarkType.bookmark_type == status)
                            .one().bookmark_type_id)

        return (User.query.join(Bookmark)
                            .filter(Bookmark.bookmark_type_id == type_id,
                                    User.user_id == Bookmark.user_id,
                                    Bookmark.event_id == self.event_id).all())


class Bookmark(db.Model):
    """User's bookmarks of specific events on jams website."""

    __tablename__ = "bookmarks"

    bookmark_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    event_id = db.Column(db.String(200), db.ForeignKey("events.event_id"), nullable=False)
    bookmark_type_id = db.Column(db.Integer, db.ForeignKey("bookmark_types.bookmark_type_id"), nullable=False)

    # # Define a relationship to user
    # # this means: put an attribute on the user class to give me bookmark objects
    # user = db.relationship("Users", backref="bookmarks")
    # # Define a relationship to events
    # event = db.relationship("Events")
    # # Define a relationship to
    bookmark_type = db.relationship("BookmarkType", backref="bookmarks")

    def __repr__(self):
        """Provide helpful representation when a bookmark is printed."""

        return "<Bookmark ID={} User ID={} Event ID={} Bookmark Type ID={}".format(self.bookmark_id, self.user_id , self.event_id, self.bookmark_type_id)


class BookmarkType(db.Model):
    """Types of bookmarks on jams website."""

    __tablename__ = "bookmark_types"

    bookmark_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    bookmark_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when a bookmark type is printed."""

        return "<Bookmark Type ID={} Bookmark Type={}".format(self.bookmark_type_id, self.bookmark_type)


class Comment(db.Model):
    """Comments on jams website."""

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # foreign key relationship takes tablename.fieldname as attributes
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    event_id = db.Column(db.String(200), db.ForeignKey('events.event_id'), nullable=False)
    comment = db.Column(db.String(800), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    # Define a relationship to user
    user = db.relationship("User", backref="comments")
    # Define a relationship to events
    event = db.relationship("Event", backref="comments")

    def __repr__(self):
        """Provide helpful representation when a comment is printed."""

        return "<Comment ID={} User ID={} Event ID {}".format(self.comment_id, self.user_id, self.event_id)


################################################################################
# Helper functions

def connect_to_db(app, db_uri=DB_URI):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively,
    # it will leave you in a state of being able to work with the database directly.
    # create a fake flask app

    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."