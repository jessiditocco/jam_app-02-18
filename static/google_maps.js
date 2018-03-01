// This is the javascript code for google maps that will display on the user profile page

"use strict";

var map;

// var marker;
// We need global array of infowindows so we can close all of the open ones
var infoWindows = [];

// Once the HTML loads, get the event details json for map (lat,long,name,address,venuename)
$(document).ready(getMapJson);

// Gets jsonified event details that we can pass to make map function, pass the users id to get their
function getMapJson(evt) {
  // We need to explicitly pass the current user id in the payload in order to use it in the map.json route
  let payload = {"user_id": $("#user_id_for_map").val()};
  $.get("/map.json", payload, createMap);
}

// Make map function that will create the map using details from the users bookmarked events
function createMap(result) {
  // This creates the map and centers the map around east Australia
  let avg_lat = result["center"]["lat"];
  let avg_long = result["center"]["long"];

  let center = {lat: avg_lat, lng: avg_long};

  map = new google.maps.Map(document.querySelector("#map"), {
    center: center, 
    zoom: 12,
  });

  // loop through each event in the result object and get data

  for (let musicEvent in result) {
    console.log(musicEvent);
    let name = result[musicEvent]["name"];
    let longitude = result[musicEvent]["longitude"];
    let latitude = result[musicEvent]["latitude"];
    let address = result[musicEvent]["address"];
    let venue_name = result[musicEvent]["venue_name"];

    let newMarker = addMarker(latitude, longitude, name);
    console.log(newMarker);
    // markersArray.push(newMarker);
    addInfoWindow(name, address, venue_name, newMarker);

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
  let marker = new google.maps.Marker({
    position: nearEvent,
    map: map, 
    title: 'Hover text', 
    icon: myImageUrl
  });
    return marker;
}


/////////////////
// info window //
/////////////////


function addInfoWindow(name, address, venue_name, marker) {

  let contentString = '<div id="content">' +
    '<h5>' + name +'</h5>' + '<p>' + 'Venue Name:' + venue_name + '</p>' + '<p>' + address + '</p>' + 
    '</div>';

  let infoWindow = new google.maps.InfoWindow({
    content: contentString,
    maxWidth: 200
  });

  infoWindows.push(infoWindow);

  marker.addListener('click', function() {
    hideAllInfoWindows(map);
    infoWindow.open(map, marker);
  });
}


function hideAllInfoWindows(map) {
  infoWindows.forEach(function(infoWindow) {
    infoWindow.close();
  });
}