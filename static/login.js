// Javascript for login and logout

function showLoginSuccess(result) {
    console.log(result);

    if (result["message"] === "success") {
        $("#close_login_modal").click();
        $("#login_button").hide();
        $("#logout_button").show();

        alert("User has been succesfully logged in");


    } else {
        $("#incorrect_login_message").html("Email/password combo incorrect. Try again please.");

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


function showLogoutSuccess(result) {
    console.log(result);
    $("#logout_button").hide();
    $("#login_button").show();
    alert("User has been succesfully logged out of session.")
}


function logoutUser(evt) {
    evt.preventDefault();

    $.get("/logout", showLogoutSuccess);
}

$("#logout_button").on("click", logoutUser);