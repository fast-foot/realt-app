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
});