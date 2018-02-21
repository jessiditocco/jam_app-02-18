/// was working on this function; get it to close after the user logs in
// if the user doesn't log in correctly, get a message to pop up saying try again

function showLoginSuccess(result) {
    console.log(result);

    if (result["message"] === "success") {
        $("#close_login_modal").click();
        alert("User has been succesfully logged in");

    }
}

function loginUser(evt) {
    evt.preventDefault();
    let payload = {
        "email": $("#login_email").val(),
        "password": $("#login_password").val()
    }
    $.post("/login", payload, showLoginSuccess);
}



$("#submit_login_button").on("click", loginUser);