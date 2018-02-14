// Javascript for posting comments on the page without reloading the page

function showComments(comment_details) {

    console.log(comment_details['comment'])
    console.log(comment_details['user_name'])

    $("#comment-list").append(
        '<li>' + comment_details["user_name"] + ": " + comment_details["comment"] + '</li>'
        );

}

function addCommentToDb(evt) {
    evt.preventDefault();
    let eventId = $(this).data("eventid");
    let payload = {
        "comment": $("#comment_text").val(),
        "event_id": eventId
    };
    console.log(payload);

    $.post("/add_comment", payload, showComments);

}

$("#comment").on("submit", addCommentToDb);