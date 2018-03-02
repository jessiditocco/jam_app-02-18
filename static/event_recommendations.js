// JS for event_recommendations

function showRecommendations(event_recommendation_details) {
    console.log(event_recommendation_details);
    // grab the div which is currently holding loading gif
    // parse the results and create DOM elements to hold them
    // replace the loading gif with those DOM elements

    // If event_recommendations exist, hide the loading gif, show event
    // recommendations, and loop through events to append details to html

    if (event_recommendation_details) {
        $("#loading_gif").hide();
        $("#event_recommendations").show();
        // Loop through and append the details for each event to HTML
        for (let event in event_recommendation_details) {
            let divId = event_recommendation_details[event]["id"];

            $("#event_recommendations").append("<div id=" + divId + " class='col-xs-6'>" +"</div>");
            $("#" + divId).append("<div class='event-name'><h3 class='child'>" + event_recommendation_details[event]["name"] + "</h3></div>");
            // $("#event_recommendations").append("<img src=" + event_recommendation_details[event]["logo"] + "/>");
            $("#" + divId).append("<a href='/event_details?event_id=" + event_recommendation_details[event]["id"] +"'><img src=" + event_recommendation_details[event]["logo"] + "/></a>");
        }


    // If event recommendations do not exits, we want to hide the loading gif & 
    //display a message to the user telling them to search events to get recommendations
    } else {
        $("#loading_gif").hide();
        $("#event_recommendations").show();
        $('#event_recommendations').append("<h5>" + "Please search some events to get recommendations" 
            + "</h5>");
    }
    

};


function getRecommendations(evt) {
    $.get("/get_recommendations.json", showRecommendations);
};


$(document).ready(getRecommendations);