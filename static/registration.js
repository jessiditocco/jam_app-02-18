// Javascript for regisration modal window

function showRegistrationSuccess(result) {
    if (result["message"] === "success") {
        $("#close_registration_modal").click();
        $("#success_div").html("User was succesfully created and logged in");
        $("#login_button").hide();
        $("#registration_button").hide();
        $("#logout_button").show();
        $("#my_profile_button").show();
        setTimeout(function() {$("#success_div").html("");}, 3000);

        // window.location = "/";
        // alert("User was succesfully created and logged in");

        
    } else {
        $("#user_in_db").html("User/password combination already exits. Please try again.");


    }
    
    console.log(result);
}


function registerUser(evt) {
    console.log("hiiiiii");
    evt.preventDefault();
    let payload = {
        "name": $("#registration_name").val(),
        "email": $("#registration_email").val(),
        "password": $("#registration_password").val(),
    };

    $.post("/register_new_user", payload, showRegistrationSuccess);

}


$("#register_user_button").on("click", registerUser);
