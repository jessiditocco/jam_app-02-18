// This is the javascript code for google maps that will display on the user profile page

"use strict";

let eastAustralia = {lat: -34.397, lng: 150.644};

let map = new google.maps.Map(document.querySelector("#map"), {
    center: eastAustralia, 
    zoom: 8, 
});

///////////////////
// Adding markers//
///////////////////

function addMarker() {
    let myImageUrl = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
    let nearSydney = new google.maps.LatLng(-34.788666, 150.41146);
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