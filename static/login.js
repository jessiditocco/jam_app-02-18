// Javascript for login and logout

function showLoginSuccess(result) {
    console.log(result);

    if (result["message"] === "success") {
        $("#close_login_modal").click();
        $("#login_button").hide();
        $("#logout_button").show();
        $("#my_profile_button").show();
        $("#success_div").html("User has been succesfully logged in.");
        setTimeout(function() {$("#success_div").html("");}, 3000);
        // // Changes url of what page you are on-- like a JS redirect
        // window.location = "/";
        


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


function showLogoutSuccess() {
    $("#success_div").html("User has been succesfully logged out.");
    $("#logout_button").hide();
    $("#login_button").show();
    $("#my_profile_button").hide();
    setTimeout(function() {$("#success_div").html("");}, 3000);
    // // Changes url of what page you are on-- like a JS redirect
    // window.location = "/";
    
}


function logoutUser(evt) {
    evt.preventDefault();

    $.get("/logout", showLogoutSuccess);
}

$("#logout_button").on("click", logoutUser);