// Javascript for regisration modal window

function showRegistrationSuccess(result) {
    if (result["message"] === "success") {
        $("#close_registration_modal").click();
        alert("User was succesfully created");
        
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
