/**
 * Created by alexei on 01.05.16.
 */

$(document).ready(function () {
    $('#filterForm #applicationType').on('change', function () {
        if ($(this).val() == "sale") {
            $("#filterForm #propertyType option:eq(2)").prop('disabled', true);
        } else if ($(this).val() == "rent") {
            $("#filterForm #propertyType option:eq(2)").prop('disabled', false);
        }
    });

    $('#apply-filter-btn').click(function () {
        console.log($('#filterForm').serialize());

        $.ajax({
                url: API_SERVER +'/filter_applications',
                data: $('#filterForm').serialize(),
                contentType: "application/x-www-form-urlencoded;charset=utf-8",
                dataType: "json",
                type: 'GET',
                success: function(response) {
                    console.log(response);
                },
                error: function(error) {
                    console.log(error);
                }
        });
    });
});