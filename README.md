# JAM.
## *Summary*
JAM. is a music-focused social network application that connects people through events using Eventbrite's API. The JAM. application allows users to search for music events by keyword, comment on events, and manage bookmarked events through their profile.

## About the Developer
JAM. was created by Jessi DiTocco, a software engineer in San Francisco, CA. [DiTocco Linkedin](https://www.linkedin.com/in/jessiditocco/ "Jessi DiTocco Linkedin")


## Tech stack 
* Python
* Flask
* Javascript (AJAX, JSON)
* PostgreSQL
* HTML
* CSS
* jQuery
* FlaskBootstrap
* FlaskJinja

## Features

### Homepage:

![alt text](https://raw.githubusercontent.com/jessiditocco/jam_app-02-18/master/readme_screenshots/homepage.png) "JAM. Homepage")

### Event Search
Once logged in to JAM., a user can search for events in their area by keyword, date, and location. The user will be redirected to an events page which is populated with event data returned from eventbrite. I built this feature by making a GET request to eventbrite's API, based on search input from the user.
![alt text](https://raw.githubusercontent.com/jessiditocco/jam_app-02-18/master/readme_screenshots/event_search.png) "Event Search Page")

### Event Details Page
From the event search page, a user can click on a specific event that they are interested in to view more details about an event. On an event details page, the user will find information about the venue, start-time, and end-time for the selected event, along with an extended description about the event. From the event details page, a user can access a bookmark feature which allows a user to pin an event as either "going" or "interested". A user will be able to manage their pinned events from their profile. Similarly, on the event details page, a user can access the comment feature where a user can connect with other JAM. users. I built this comment feature by saving my comments in a comments table in my jams database and populating the page with the comments on the initial page load. I used javascript to load a current user's new comment immediatley on "submit", without having to reload the page.

![alt text](https://raw.githubusercontent.com/jessiditocco/jam_app-02-18/master/readme_screenshots/event_details.png) "Event Details Page")

### Emailing Feature
On the event details page, we can click onto another user's profile who has also bookmarked the event as "going" in order to access an emailing feature. I built this emailing feature using SendGrid's API to send an email from one user directly to another user through the JAM. platform. 


![alt text](https://raw.githubusercontent.com/jessiditocco/jam_app-02-18/master/readme_screenshots/email.png) "Emailing Feature")

### Profile
If we go back to the user's profile, we can view a list of events that a user has pinned as "going" and a list of events that a user has pinned as "interested". On the profile, we also can view a map that shows events that the user has bookmarked as "going". 

![alt text](https://raw.githubusercontent.com/jessiditocco/jam_app-02-18/master/readme_screenshots/profile.png) "Profile")

### Event Recommendations
On the homepage, a user can view a list of recommended events based on the user's past search history. I built this feature by saving a users past searches in my database, written in SQL Alchemy, and using these saved searches to make a batched API request to eventbrite's API.

![alt text](https://raw.githubusercontent.com/jessiditocco/jam_app-02-18/master/readme_screenshots/event_recommendations.png) "Event Recommendations")

