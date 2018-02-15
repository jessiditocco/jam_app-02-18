import unittest
from flask import session

from server import app
from model import db, connect_to_db

from test_model import *

# Simple flask tests testing that routes render correct HTML
class SimpleFlaskTests(unittest.TestCase):

    def setUp(self):
        """To do before every test."""
        # Create a client and bind it to self
        # I want a fresh test client for every single test
        self.client = app.test_client()
        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_homepage(self):
        """Tests that the homepage flask route works"""

        result = self.client.get("/")
        # Status code 200: OK
        self.assertEqual(result.status_code, 200)
        self.assertIn('Search', result.data)

    def test_registration(self):
        """Tests that registration form route works."""

        result = self.client.get("/register")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Name", result.data)
        self.assertIn("Email", result.data)

   


# Flask tests that require the user to be logged in to the session
class FlaskTestsLoggedIn(unittest.TestCase):
    """Tests the require the user to be logged in."""

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'

        # Creates a test client
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1

    def test_navbar_for_session(self):
        """Checks that the navbar displays logout and not login if the user is 
        in the session."""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Logout", result.data)
        self.assertNotIn("Login", result.data)

    def test_logout(self):
        """Test the logout route to ensure logout message gets flashed and user 
        is redirected to homepage"""

        result = self.client.get("logout", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("User has been successfully logged out", result.data)



# Flask tests that make calls to the database
class FlaskTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Sets up the db before each test is called."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to the test db
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Tears the database down after each test is called."""

        db.session.close()
        db.drop_all()

    def test_login(self):
        """Tests login if user exists in database"""

        result = self.client.post("/login", data={"user_id": "1", "email": "jessi.ditocco@gmail.com", 
            "password": "jessi"}, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Search", result.data)

    def test_login_fail(self):
        """Checks that user cannot register if login email/pword combo isn't in db"""


        result = self.client.post("/login", data={"user_id": "3", 
            "email": "doesnotexist@gmail.com", "password": "test"}, 
            follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("User Login", result.data)



if __name__ == "__main__":
    import unittest

    unittest.main()