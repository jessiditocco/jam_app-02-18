// JS for event_recommendations

function showRecommendations(event_recommendation_details) {
    console.log(event_recommendation_details);
    // grab the div which is currently holding loading gif
    // parse the results and create DOM elements to hold them
    // replace the loading gif with those DOM elements

    $("#loading_gif").hide();
    $("#event_recommendations").show();

    for (let event in event_recommendation_details) {
        $("#event_recommendations").append("<p>" + event_recommendation_details[event]["name"] + "</p>");
        $("#event_recommendations").append("<p>" + event_recommendation_details[event]["id"] + "</p>");
        $("#event_recommendations").append("<img src=" + event_recommendation_details[event]["logo"] + "/>");

    }

    
    // $("#event_recommendations").append("<p>" + event_recommendation_details["Event1"]["name"] +"</p>");

    console.log($("#event_recommendations").html());


};


function getRecommendations(evt) {
    $.get("/get_recommendations.json", showRecommendations);
};


$(document).ready(getRecommendations);