# Import os so that we can create db
import os
from model import BookmarkType, User, db, connect_to_db

def load_bookmark_types():
    """Seed bookmark type data into jams db."""

    going = BookmarkType(bookmark_type="going")
    interested = BookmarkType(bookmark_type="interested")
    db.session.add_all([going, interested])
    db.session.commit()

def load_jam_users():
    """Seed fake users into jams db."""
    
    user1 = User(email="jessica.ditocco@ufl.edu", name="Jessi DiTocco", password="test")
    user2 = User(email="jessi.ditocco@gmail.com", name="Jane Doe", password="test")
    user3 = User(email="twonaroll@yahoo.com", name="Liz Lee", password="test")
    db.session.add_all([user1, user2, user3])
    db.session.commit()

if __name__ == "__main__":
    # Create the database
    os.system("createdb jams")

    # Connect the DB to an app so FlaskSQL alchemy works
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)

    # Create the tables
    db.create_all()

    # Add the bookmark types
    load_bookmark_types()
    load_jam_users()