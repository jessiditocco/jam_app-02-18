// Document ready prevents JS from loading until all HTML has loaded

$(document).ready(
    function() {
    $(".bookmark").on("click", function(evt) {
    let eventId = $(this).data("eventid");
    let status = $(this).data("status");
    let payload = {"event_id": eventId,
                   "status": status,
                   "name": $("#name").html(),
                   "start_time": $('#start_time').html(),
                   "end_time": $('#end_time').html(),
                   "address": $('#address').html(),
                   "latitude": $('#latitude').html(),
                   "longitude": $('#longitude').html(),
                   "eb_url": $('#eb_url').html(),
                   "description": $("#description").html(),
                   "venue_name": $("#venue_name").html(), 
                   "logo": $("#logo").html()};

    $.post("/add_bookmark", payload, function (results) {
        alert(results);

    });


});
});