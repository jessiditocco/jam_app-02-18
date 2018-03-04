// Javascript for seding email to users from the profile page

function showSuccess(success_message) {
    $("#close_modal").click();
    console.log(success_message);
    $("#email_success_div").html(success_message);
    $("#email_success_div").show();
    setTimeout(function () {$("#email_success_div").hide();} , 3000);


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