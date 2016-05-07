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
                    contentType: "application/x-www-form-urlencoded;charset=utf-8",
                    dataType: "json",
                    type: 'POST',
                    success: function(response) {
                        if (response['success'] === "true") {
                            $('.reg-form').trigger('reset');
                            $('#popup-title').text('Регистрация прошла успешно!');
                            $('#popup-message').text("Используйте логин и пароль для входа на сайт.");
                            $('#myModal').modal();
                        } else if (response['success'] === "false") {
                            $('#popup-title').text('Регистрация не была пройдена');
                            $('#popup-message').text("Пользователь с таким логином уже существует.");
                            $('#myModal').modal();
                        }
                        console.log(response);
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            } else {
                $('#popup-title').text('Ошибка ввода');
                $('#popup-message').text("Проверьте правильность введенного email");
                $('#myModal').modal();
            }
        } else {
            $('#popup-title').text('Ошибка ввода');
            $('#popup-message').text("Пароли не совпадают");
            $('#myModal').modal();
        }
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
            type: 'PUT',
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
            var role = $('input[name=role]:checked').val();
            var editedRowIndex = $('#editUserForm #selectedRowIndex').val();

            $("tr#userEditRow").eq(editedRowIndex).find('td').eq(0).text(login);
            $("tr#userEditRow").eq(editedRowIndex).find('td').eq(1).text(fname);
            $("tr#userEditRow").eq(editedRowIndex).find('td').eq(2).text(lname);
            $("tr#userEditRow").eq(editedRowIndex).find('td').eq(3).text(email);
            $("tr#userEditRow").eq(editedRowIndex).find('td').eq(4).text(phone_number);
            $("tr#userEditRow").eq(editedRowIndex).find('td').eq(5).text(birthday);
            if(role == 1){
                $("tr#userEditRow").eq(editedRowIndex).find('td').eq(7).text("Пользователь");
            }
            else{
                $("tr#userEditRow").eq(editedRowIndex).find('td').eq(7).text("Администратор");
            }
        });
    });

    $('#edit-private-user-btn').click(function() {
        $.ajax({
            url: API_SERVER + '/user/' + $('#editPrivateUserForm #user_id').val(),
            data: $('#editPrivateUserForm').serialize(),
            type: 'PUT',
        }).done(function(data) {
            console.log(data);
            $('#popup-title').text('Данные были изменены');
            $('#popup-message').text("Редактирование прошло успешно.");
            $('#myModal').modal();
        }).fail(function (e) {
            console.log('error');
        });
    });

    $("#deleteUsersBtn").click(function(){
        var usersIdToDelete = "";

        $("tr#userEditRow").each(function() {

            if ( $(this).find('input[type=checkbox]').is(':checked') ) {
                usersIdToDelete += $(this).find('td').eq(6).text() + ",";
                $(this).remove();
            }
        });

        if (usersIdToDelete === "") {
            $('#popup-title').text('Не выбран пользователь');
            $('#popup-message').text("Для удаления необходимо выбрать хотя бы одного пользователя");
            $('#myModal').modal();
        }
        else {
            usersIdToDelete = usersIdToDelete.slice(0, usersIdToDelete.length - 1);

            $.ajax({
                url: API_SERVER + '/user/' + usersIdToDelete,
                type: 'DELETE',
            }).done(function(data) {
                console.log(data);
            }).fail(function (e) {
                console.log('error');
            })
        }
    });

    /*/Edit user in admin mode*/

    $('#delete-app-btn').click(function() {
    var appIdsToDelete = "";

        $("tr.appRowInAdminMode").each(function() {
            if ( $(this).find('input[type=checkbox]').is(':checked') ) {
                appIdsToDelete += $(this).find('td').eq(0).text() + ",";
                $(this).remove();
            }
        });
        console.log('del = '+appIdsToDelete);
        appIdsToDelete = appIdsToDelete.slice(0, appIdsToDelete.length - 1);

        $.ajax({
                url: API_SERVER +'/applications',
                data: {"app_ids": appIdsToDelete},
                contentType: "application/x-www-form-urlencoded;charset=utf-8",
                dataType: "json",
                type: 'DELETE',
                success: function(response) {
                    console.log(response);
                },
                error: function(error) {
                    console.log(error);
                }
        });
    });

    $('tr.appRowInUserMode, tr.appRowInAdminMode').click(function() {
        var app_id = $(this).find('td:eq(0)').text();
        var user_id = $('#viewed_user_id').val();

        $.ajax({
                url: API_SERVER +'/application',
                data: {"app_id": app_id, "viewed_user_id": user_id},
                contentType: "application/x-www-form-urlencoded;charset=utf-8",
                dataType: "json",
                type: 'GET',
                success: function(response) {
                    console.log(response);
                    $('.app-content').empty();
                    line = "";
                    $.each(response, function(k, v) {
                        if (v instanceof Array) {
                            line = "<p><strong>"+k+":</strong> ";

                            for (var feature_index in v) {
                                console.log(v[feature_index]);
                                line += v[feature_index] + ", ";
                            }

                            line = line.slice(0, -2);
                            line += "</p>"
                        } else {
                            console.log(k);
                            if (v != null) {
                                line = "<p><strong>"+k+":</strong> "+v;
                                if (k.indexOf("Площадь") > -1) {
                                    line += " м<sup>2</sup>";
                                } else if (k.indexOf("Цена") > -1) {
                                    line += " у.е.";
                                }
                                line += "</p>";
                            } else {
                                line = "<p><strong>"+k+":</strong> не указано"+"</p>";
                            }
                        }
                        $('.app-content').append(line);
                        if (k.indexOf("Цена") > -1) {
                            line = "<p><strong>Цена за 1 м<sup>2</sup>:</strong> " + (v / response['Площадь общая']).toFixed(2) + " у.е";
                            $('.app-content').append(line);
                        }
                    });

                },
                error: function(error) {
                    console.log(error);
                }
        });

    });
});


/*applications in admin profile*/

function changeApplicationStatus(status) {
    var appIdsToEdit = "";

        $("tr.appRowInAdminMode").each(function() {

            if ( $(this).find('input[type=checkbox]').is(':checked') ) {
                appIdsToEdit += $(this).find('td').eq(0).text() + ",";
                if (status == 1) {
                    $(this).find('td:eq(6)').text("Подтверждено");
                } else if (status == 0) {
                    $(this).find('td:eq(6)').text("Не подтверждено");
                } else {
                    $(this).find('td:eq(6)').text("Отклонено");
                }
            }
        });

        appIdsToEdit = appIdsToEdit.slice(0, appIdsToEdit.length - 1);

        $.ajax({
                url: API_SERVER +'/applications',
                data: {"app_ids": appIdsToEdit, "app_status": status},
                contentType: "application/x-www-form-urlencoded;charset=utf-8",
                dataType: "json",
                type: 'PUT',
                success: function(response) {
                    console.log(response);
                },
                error: function(error) {
                    console.log(error);
                }
        });
}



/*/applications in admin profile*/
