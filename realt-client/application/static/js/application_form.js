$(document).ready(function() {

    $('#applicationType').on('change', function() {
        if ($(this).val() === "rent") {
            $('#featuresSection').show();
            $("#propertyType option:eq(2)").prop('disabled', false);
        } else {
            $('#featuresSection').hide();
            $("#propertyType option:eq(2)").prop('disabled', true);
            $("#propertyType").prop('selectedIndex', 0);
            $('#featuresSection label input[type=checkbox]').each(function() {
                $(this).prop('checked', false);
            });
        }
    });

    $('#propertyType').on('change', function() {
        selectedProperty = $(this).find('option:selected').text();

        if (selectedProperty === "Дом") {
            $('#applicationForm #floor').prop('disabled', true);
            $('#applicationForm #floor').val('');
            $('#applicationForm #live_square').prop('disabled', false);
            $('#applicationForm #kitchen_square').prop('disabled', false);
        } else if (selectedProperty === "Квартира") {
            $('#applicationForm #floor').prop('disabled', false);
            $('#applicationForm #live_square').prop('disabled', false);
            $('#applicationForm #kitchen_square').prop('disabled', false);
        } else {
            $('#applicationForm #floor').prop('disabled', false);
            $('#applicationForm #live_square').prop('disabled', true);
            $('#applicationForm #live_square').val('');
            $('#applicationForm #kitchen_square').prop('disabled', true);
            $('#applicationForm #kitchen_square').val('');
        }
    });

    $('#sendApplicationBtn').click(function () {
        console.log($('#applicationForm').serialize());
       $.ajax({
            url: API_SERVER + '/application',
            data: $('#applicationForm').serialize(),
            contentType: "application/x-www-form-urlencoded;charset=utf-8",
            dataType: "json",
            type: 'POST',
        }).done(function(data) {
            console.log(data);

        }).fail(function (e) {
            console.log('error');
        });
    });
});