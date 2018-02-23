// JS for event_recommendations

function showRecommendations(results) {
    console.log(results);
    // grab the div which is currently holding loading gif
    // parse the results and create DOM elements to hold them
    // replace the loading gif with those DOM elements

    console.log($("#event_recommendations").html());

    $("#event_recommendations").append("<p>" + results["test"] +"</p>");

    console.log($("#event_recommendations").html());


};


function getRecommendations(evt) {
    $.get("/get_recommendations.json", showRecommendations);
};


$(document).ready(getRecommendations);