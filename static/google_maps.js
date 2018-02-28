// This is the javascript code for google maps that will display on the user profile page

"use strict";

var map;
var marker;

// Once the HTML loads, get the event details json for map
$(document).ready(getMapJson);

// Gets jsonified event details that we can pass to make map function
function getMapJson(evt) {
  // We need to explicitly pass the current user id in the payload in order to use it in the map.json route
  let payload = {"user_id": $("#user_id_for_map").val()};
  $.get("/map.json", payload, createMap);
}

// Make map function that will create the map using details from the users bookmarked events
function createMap(result) {
  // This creates the map and centers the map around east Australia
  let sanFrancisco = {lat: 37.773972, lng: -122.431297};

  map = new google.maps.Map(document.querySelector("#map"), {
    center: sanFrancisco, 
    zoom: 8,
  });

  // loop through each event in the result object and get data

  for (let musicEvent in result) {
    console.log(musicEvent);
    let name = result[musicEvent]["name"];
    let longitude = result[musicEvent]["longitude"];
    let latitude = result[musicEvent]["latitude"];
    let address = result[musicEvent]["address"];
    let venue_name = result[musicEvent]["venue_name"];

    addMarker(latitude, longitude, name);

    // addInfoWindow(name, venue_name, address);
  }
}

///////////////////
// Adding markers//
///////////////////

function addMarker(latitude, longitude, name) {
  // console.log(latitude, longitude, name);
  let myImageUrl = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
  let nearEvent = new google.maps.LatLng(latitude, longitude);
  console.log(nearEvent);
  marker = new google.maps.Marker({
    position: nearEvent,
    map: map, 
    title: 'Hover text', 
    icon: myImageUrl
  });
    // marker.setMap(map);
    return marker;
}


/////////////////
// info window //
/////////////////

function addInfoWindow() {

  let contentString = '<div id="content">' +
    '<h1>All my custom content</h1>' +
    '</div>';

  let infoWindow = new google.maps.InfoWindow({
    content: contentString,
    maxWidth: 200
  });

  marker.addListener('click', function() {
    infoWindow.open(map, marker);
  });
}

// let infoWindow = addInfoWindow();