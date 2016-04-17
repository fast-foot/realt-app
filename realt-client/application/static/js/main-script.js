const API_SERVER = 'http://127.0.0.1:5000';
const CLIENT_SERVER = 'http://0.0.0.0:4992';

$(document).ready(function () {

    $('#reg-btn').click(function() {
        console.log($('.reg-form').serialize());
        $.ajax({
            url: API_SERVER +'/users',
            data: $('.reg-form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('#login-btn').click(function () {
        $.ajax({
            url: CLIENT_SERVER + '/login',
            data: $('#logInForm').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });

        /*$.getJSON($SCRIPT_ROOT + '/login', {
            login: $('#logInForm #login').val(),
            password: $('#logInForm #password').val()
        }, function(data) {
              console.log(data.result);
           });*/

    });
});
