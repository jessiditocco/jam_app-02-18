// JS for event_recommendations

function showRecommendations(event_recommendation_details) {
    console.log(event_recommendation_details);
    // grab the div which is currently holding loading gif
    // parse the results and create DOM elements to hold them
    // replace the loading gif with those DOM elements

    $("#loading_gif").hide();
    $("#event_recommendations").show();

    // If event recommendation_details exits
    // Loop through and append the details for each event to HTML
    for (let event in event_recommendation_details) {
        $("#event_recommendations").append("<p>" + event_recommendation_details[event]["name"] + "</p>");
        $("#event_recommendations").append("<p>" + event_recommendation_details[event]["id"] + "</p>");
        $("#event_recommendations").append("<img src=" + event_recommendation_details[event]["logo"] + "/>");
    }
};


function getRecommendations(evt) {
    $.get("/get_recommendations.json", showRecommendations);
};


$(document).ready(getRecommendations);