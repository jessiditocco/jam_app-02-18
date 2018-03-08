# Jam
## *Summary*
Jam is a music-focused social network application that connects people through events using Eventbrite's API. The Jam application allows users to search for music events by keyword, comment on events, and manage bookmarked events through their profile.

## About the Developer
Jam was created by Jessi DiTocco, a software engineer in San Francisco, CA. [DiTocco Linkedin](https://www.linkedin.com/in/jessiditocco/ "Jessi DiTocco Linkedin")


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

Inline-style: 
![alt text](https://raw.githubusercontent.com/jessiditocco/jam_app-02-18/master/readme_screenshots/homepage.png) "Jam Homepage")

Once logged in, a user can search for events in their area by keyword, date, and location. The user will be redirected to an events page which is populated with events returned from eventbrite. I built this feature by making a GET request to eventbrite based on search criteria, and then returning to the user, data about events in their area that match the searched criteria. 

Inline-style: 
![alt text](https://raw.githubusercontent.com/jessiditocco/jam_app-02-18/master/readme_screenshots/event_search.png) "Event Search Page")

From the event search page, a user can click on a specific event that they are interested in in order to view more details about an event. On an event details page, the user will find information about the venue, start-time, and end-time for the selected event, along with a description about the event. From the event details page, a user can access a bookmark feature which allows a user to pin an event as either "going" or "interested". A user will be able to manage their pinned events from their profile. Similarly, on the event details page, a user can access the commenting feature where a user can connect with other jam users by commenting on events. I built this comment feature by saving my comments in a comments table in my Jams database and populating the page with the comments on the initial page load. I used javascript to load a users new comment on "submit", without reloading the page. 

Inline-style: 
![alt text](https://raw.githubusercontent.com/jessiditocco/jam_app-02-18/master/readme_screenshots/event_details.png) "Event Details Page")

On the event details page, we can click onto another user's profile who has also bookmarked the event as "going" in order to access an emailing feature. I built this emailing feature using SendGrid's API to send an email from one user directly to another user through the Jam platform. 


Inline-style: 
![alt text](https://raw.githubusercontent.com/jessiditocco/jam_app-02-18/master/readme_screenshots/email.png) "Event Details Page")

If we go back to the user's profile, we can view a list of events that a user has pinned as "going" and a list of events that a user has pinned as "interested". On the profile, we also can view a map that shows the users events that that have pinned as "going". 

Inline-style: 
![alt text](https://raw.githubusercontent.com/jessiditocco/jam_app-02-18/master/readme_screenshots/profile.png) "Event Details Page")


Inline-style: 
![alt text](https://raw.githubusercontent.com/jessiditocco/jam_app-02-18/master/readme_screenshots/email.png) "Event Details Page")



Once logged in, the user can access their profile page to view a list of bookmarked events, as well as a map of bookmarked events, built using the Google Maps API. Users can connect with other Jam users via an email feature on the Jam application that uses SendGrid's emailing API. On the homepage, a user can view a list of recommended events based on the user's past search history. I built this feature by saving a users past searches in my database, written in SQL Alchemy, and using these saved searches to make a batched API request to eventbrite.
