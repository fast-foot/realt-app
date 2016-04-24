$(document).ready(function() {

    $('#applicationType').on('change', function() {
        if ($(this).val() === "rent") {
            $('#features').show();
            $("#propertyType option[value='room']").removeAttr('disabled');
        } else {
            $('#features').hide();
            $("#propertyType option[value='room']").attr('disabled', 'disabled');
        }
    });

    $('#propertyType').on('change', function() {
        if ($(this).val() === "house") {
            $('#applicationForm #floor').prop('disabled', true);
            $('#applicationForm #live_square').prop('disabled', false);
            $('#applicationForm #kitchen_square').prop('disabled', false);
        } else if ($(this).val() === "flat") {
            $('#applicationForm #floor').prop('disabled', false);
            $('#applicationForm #live_square').prop('disabled', false);
            $('#applicationForm #kitchen_square').prop('disabled', false);
        } else {
            $('#applicationForm #floor').prop('disabled', false);
            $('#applicationForm #live_square').prop('disabled', true);
            $('#applicationForm #kitchen_square').prop('disabled', true);
        }
    });

    $('#sendApplicationBtn').click(function () {
       $.ajax({
            url: API_SERVER + '/application_data',
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
});