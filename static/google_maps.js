// This is the javascript code for google maps that will display on the user profile page

"use strict";

// This function initializes a map with lat longs
function initMap() {
    let uluru = {lat: -25.363, lng: 131.044};
    let map = new google.maps.Map(document.querySelector('#map'), {
        zoom: 4,
        center: uluru
    });

    let marker = new google.maps.Marker({
        position: uluru,
        map: map, 
        title: "Hover Text",
        // icon: myImageUrl
    });
}