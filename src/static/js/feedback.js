/**
 *This script submits the user's login credentials and gives feedback if login fails
 If login is successful, user is redirected to Device page 
 */

$(document).ready(function () {
    $('#feedback').hide() //Hide the 'message' div when the page loads
});


/*For retrieving CSRF token
  https://docs.djangoproject.com/en/1.11/ref/csrf/
*/
function get_cookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Get current URL
function get_current_url() {
    var current_url = '';
    if (window.location.href == '/') {
        current_url = '/auth_app/user_login';
    } else if (window.location.href == '/register/') {
        current_url = '/register/';
    }
    return current_url;
}

/*================For AJAX post=================*/


// When login form is submitted
$(document).on('submit', '#login', function (event) {

    //Prevent default submit behavior
    event.preventDefault();

    //Prepare csrf token
    var csrftoken = get_cookie('csrftoken');

    //Collect data from form fields
    var username = $('#username').val();
    var password = $('#password').val();


    //Send data to View
    $.ajax({
        url: get_current_url(),
        type: "POST",
        data: {
            csrfmiddlewaretoken: csrftoken,
            username: username,
            password: password,
        }, // data sent with the POST request

        //Successful response
        success: function (responseData) {
            //On success show the data posted to server as a message
            if (responseData['results'] == 'failed') {
                $('#feedback').html(responseData['message']).show();
            } else if (responseData['results'] == 'success') {
                location.href = "/podrequest/";
            }
        },

        //Non-successful response
        error: function (data) {
            //On failed response, give user a message
            alert("Something went wrong.");
        }
    });
});
