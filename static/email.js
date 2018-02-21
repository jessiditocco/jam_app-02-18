// Javascript for posting comments on the page without reloading the page

function showSuccess(success) {
    $("#close_modal").click();
    console.log(success);
    alert("You have succesfully sent an email!");

}

function sendEmail(evt) {
    console.log('foo');
    evt.preventDefault();

    let payload = {
        "subject": $("#subject").val(),
        "email_body": $("#email_body").val(),
        "send_to": $("#send_to").val()
    };
    console.log(payload);

    $.post("/email", payload, showSuccess);

}


$("#email_user_button").on("click", sendEmail);