// This is the javascript code for google maps that will display on the user profile page

"use strict";

let map;

// Once the HTML loads, get the event details json for map
$(document).ready(getMapJson);

// Gets jsonified event details that we can pass to make map function
function getMapJson(evt) {
  $.get("/map.json", createMap);
}

// Make map function that will create the map using details from the users bookmarked events
function createMap(result) {
  // This creates the map and centers the map around east Australia
  let eastAustralia = {lat: 37.773972, lng: -122.431297};

  map = new google.maps.Map(document.querySelector("#map"), {
    center: eastAustralia, 
    zoom: 8,
  });

  console.log(result);
  // loop through each event in the result object and get data

  for (let musicEvent in result) {
    let name = result[musicEvent]["name"];
    let longitude = result[musicEvent]["longitude"];
    let latitude = result[musicEvent]["latitude"];
    let address = result[musicEvent]["address"];
    let venue_name = result[musicEvent]["venue_name"];

    // addMarker(latitude, longitude, name);
    // addInfoWindow(name, venue_name, address);
  }
}

///////////////////
// Adding markers//
///////////////////

function addMarker() {
    let myImageUrl = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
    let nearSydney = new google.maps.LatLng(37.773972, -122.431297);
    let marker = new google.maps.Marker({
        position: nearSydney,
        map: map, 
        title: 'Hover text', 
        icon: myImageUrl
    });
    return marker;
}

let marker = addMarker();

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

let infoWindow = addInfoWindow();