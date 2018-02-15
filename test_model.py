# Create sample data for tests.py to use
from model import User, Event, BookmarkType, Comment, Bookmark, db


def example_data():
    """Create some sample data for tests file to use."""

    # Create some fake users
    u1 = User(user_id=1, email="jessi.ditocco@gmail.com", name="Jessi DiTocco",
        password="jessi")
    u2 = User(user_id=2, email="liz.lee@gmail.com", name="Liz Lee",
        password="liz")

    # Create some fake events
    e1 = Event(event_id="43104373341", name="Aristophanes @ Cafe du Nord", start_time="Friday, February 16 at 9:30PM+", 
        end_time="Saturday, February 17 at 2:00AM", address="2174 Market Street, San Francisco, CA 94114",
        latitude=37.7649659, longitude=-122.431, venue_name="Slate")
    e2 = Event(event_id="41465350981", name="Funk", start_time="Friday, February 15 at 9:30PM+", 
        end_time="Saturday, February 18 at 2:00AM", address="4123 Market Street, San Francisco, CA 94114",
        latitude=39.7649659, longitude=-122.431, venue_name="The Jam")

    # Create some bookmark types
    bt1 = BookmarkType(bookmark_type_id=1, bookmark_type="going")
    bt2 = BookmarkType(bookmark_type_id=2, bookmark_type="interested")

    # Create some fake bookmarks
    b1 = Bookmark(bookmark_id=1, user_id=1, event_id="43104373341", bookmark_type_id=2)
    b2 = Bookmark(bookmark_id=2, user_id=2, event_id="43104373341", bookmark_type_id=1)


    # Create some fake Comments
    c1 = Comment(comment_id=1, user_id=1, event_id="43104373341", comment="HI!")
    c2 = Comment(comment_id=2, user_id=2, event_id="43104373341", comment="HI!")

    db.session.add_all([u1, u2, e1, e2, bt1, bt2, b1, b2, c1, c2])
    db.session.commit()
    