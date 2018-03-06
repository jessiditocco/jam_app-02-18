
// Javascript for posting comments on the page without reloading the page

function showComments(comment_details) {
    console.log(comment_details);
    // $("#comment-list").append(
    //     '<li>' + comment_details["user_name"] + ": " + comment_details["comment"] + '</li>'
    //     );
    $("#comment_text").val("");
    $("#comment-list").append('<blockquote><a href="/profile?user_id=' + comment_details.user_id + '">' + comment_details.user_name 
        + ':</a>' + '  "' + comment_details.comment + '"</blockquote>');

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