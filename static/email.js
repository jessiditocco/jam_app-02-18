// Javascript for posting comments on the page without reloading the page

function showSuccess(success) {
    $("#close_modal").click();
    console.log(success);
    alert("Hiii!!");

}

function sendEmail(evt) {
    console.log('foo');
    evt.preventDefault();

    let payload = {
        "subject": $("#subject").val(),
        "comment": $("#comment").val(),
        "send_to": $("#send_to").val()
    };
    console.log(payload);

    $.post("/email", payload, showSuccess);

}


$("#modal_button").on("click", sendEmail);