$(document).ready(function () {
    $('#feedback').hide()
});


//For getting CSRF token
function getCookie(name) {
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

//For doing AJAX post

//When submit is clicked
$(document).on('submit', '#login', function (e) {

    //Prevent default submit. Important for AJAX post.
    e.preventDefault();

    //Prepare csrf token
    var csrftoken = getCookie('csrftoken');


    //Collect data from fields
    var username = $('#username').val();
    var password = $('#password').val();

    //This is the Ajax post.Observe carefully. It is nothing but details of where_to_post,what_to_post
    //Send data  
    $.ajax({
        url: '/auth_app/user_login/', // the endpoint,commonly same url
        type: "POST", // http method
        data: {
            csrfmiddlewaretoken: csrftoken,
            username: username,
            password: password,
        }, // data sent with the post request

        // handle a successful response
        success: function (responseData) {
            console.log(responseData); // another sanity check
            //On success show the data posted to server as a message
            if (responseData['results'] == 'failed') {
                $('#feedback').html(responseData['message']).show();
            } else if (responseData['results'] == 'success') {
                location.href = "/podrequest/"
            }
        },

        // handle a non-successful response
        error: function (data) {
            console.log(data); // another sanity check
            //On success show the data posted to server as a message
            $('#feedback').html(data['message']).show();
        }
    });
});