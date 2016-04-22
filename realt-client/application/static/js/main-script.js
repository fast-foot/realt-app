const API_SERVER = 'http://127.0.0.1:5000';
const CLIENT_SERVER = 'http://0.0.0.0:4992';

$(document).ready(function () {

    var emailMask = /^[A-Z0-9._%+-]+@([A-Z0-9-]+\.)+[A-Z]{2,4}$/i;

    jQuery(function($){
        $("#phoneNumber").mask("+999 99 999-99-99");
        $("#birthday").mask("99.99.9999");
    });

    $('#reg-btn').click(function() {
        if($('#password1').val() == $('#password2').val()){
            if(emailMask.test($('#email').val())) {
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
            } else {
                $('#text_for_error').text("Проверьте правильность введенного email");
                $('#myModal').modal();
            }
        } else {
            $('#text_for_error').text("Пароли не совпадают");
            $('#myModal').modal();
        }
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

    });

    /*Edit user in admin mode*/

    /*populate userEditForm with values from users table*/
    $("tr#userEditRow").click(function(){
        var login = $(this).find('td').eq(0).text();
        var fname = $(this).find('td').eq(1).text();
        var lname = $(this).find('td').eq(2).text();
        var email = $(this).find('td').eq(3).text();
        var phone_number = $(this).find('td').eq(4).text();
        var birthday = $(this).find('td').eq(5).text();
        var user_id = $(this).find('td').eq(6).text();

        $('#editUserForm #login').val(login);
        $('#editUserForm #firstname').val(fname);
        $('#editUserForm #lastname').val(lname);
        $('#editUserForm #email').val(email);
        $('#editUserForm #phone_number').val(phone_number);
        $('#editUserForm #birthday').val(birthday.trim());
        $('#editUserForm #user_id').val(user_id);
        $('#editUserForm #selectedRowIndex').val($(this).index());

    });

    $('#edit-user-btn').click(function() {
        $.ajax({
            url: API_SERVER + '/user/' + $('#editUserForm #user_id').val(),
            data: $('#editUserForm').serialize(),
            type: 'POST',
        }).done(function(data) {
            console.log(data);
        }).fail(function (e) {
            console.log('error');
        }).always(function () {
            var login = $('#editUserForm #login').val();
            var fname = $('#editUserForm #firstname').val();
            var lname = $('#editUserForm #lastname').val();
            var email = $('#editUserForm #email').val();
            var phone_number = $('#editUserForm #phone_number').val();
            var birthday = $('#editUserForm #birthday').val();
            var editedRowIndex = $('#editUserForm #selectedRowIndex').val();

            $("tr#userEditRow").eq(editedRowIndex).find('td').eq(0).text(login);
            $("tr#userEditRow").eq(editedRowIndex).find('td').eq(1).text(fname);
            $("tr#userEditRow").eq(editedRowIndex).find('td').eq(2).text(lname);
            $("tr#userEditRow").eq(editedRowIndex).find('td').eq(3).text(email);
            $("tr#userEditRow").eq(editedRowIndex).find('td').eq(4).text(phone_number);
            $("tr#userEditRow").eq(editedRowIndex).find('td').eq(5).text(birthday);
        });
    });
    /*/Edit user in admin mode*/
});
