/**
 * Created by alexei on 01.05.16.
 */

String.prototype.format = function () {
  var args = arguments;
  return this.replace(/\{(\d+)\}/g, function (m, n) { return args[n]; });
};

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

        if ($('#filterCity').val() === "" && $('#filterStreet').val() != "") {
            $('#popup-title').text('Введите название города');
            $('#popup-message').text("Для фильтрации по названию улицы необходимо ввести название города.");
            $('#myModal').modal();
        } else {
            $.ajax({
                url: API_SERVER +'/filter_applications',
                data: $('#filterForm').serialize(),
                contentType: "application/x-www-form-urlencoded;charset=utf-8",
                dataType: "json",
                type: 'GET',
                success: function(response) {
                    console.log(response);
                    updateApplicationsTable(response);
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
    });

    $('#apply-sort-btn').click(function () {
        console.log($('#sortForm').serialize())
        $.ajax({
                url: API_SERVER +'/sort_applications',
                data: $('#sortForm').serialize(),
                contentType: "application/x-www-form-urlencoded;charset=utf-8",
                dataType: "json",
                type: 'GET',
                success: function(response) {
                    console.log(response);
                    updateApplicationsTable(response);
                },
                error: function(error) {
                    console.log(error);
                }
        });
    });

    $('#reset-filter-btn').click(function () {
        resetFilterInputs();

        $.ajax({
                url: API_SERVER +'/filter_applications',
                data: $('#filterForm').serialize(),
                contentType: "application/x-www-form-urlencoded;charset=utf-8",
                dataType: "json",
                type: 'GET',
                success: function(response) {
                    console.log(response);
                    updateApplicationsTable(response);
                },
                error: function(error) {
                    console.log(error);
                }
        });
    });

    function updateApplicationsTable(response) {
        $('#publicApplicationsTable').find("tr:gt(0)").remove();

        $.each(response, function (k, applications) {
           var rowNumber = 1;

           for (var key in applications) {
               console.log(applications[key]);
               var application = applications[key];
               var appId = application['id'];
               var appType = application['type'];
               var propType = application['property_type'];
               var address = application['address'];
               var price = application['price'];
               var createdDate = application['created_date'];
               var viewCount = application['view_count'];

               createAppTableRow(appId, rowNumber, appType, propType, address, price, createdDate, viewCount);

               rowNumber += 1;
           }
        });
        $('#publicApplicationsTable tbody tr td').attr('data-toggle', 'modal');
        $('#publicApplicationsTable tbody tr td').attr('data-target', '.app-content-modal');
    }

    function createAppTableRow(id, rowNumber, appType, propType, address, price, createdDate, viewCount) {
        var start = '<tr class="appRowInUserMode">';
        var idCol = '<td style="display: none;">{0}</td>'.format(id);
        var rowNumberCol = '<td>{0}</td>'.format(rowNumber);
        var propTypeCol = '<td>{0}</td>'.format(propType);
        var addressCol = '<td>{0}</td>'.format(address);
        var priceCol = '<td>{0}</td>'.format(price);
        var createdDateCol = '<td>{0}</td>'.format(createdDate);
        var viewCountCol = '<td>{0}</td>'.format(viewCount);
        var appTypeCol = '';

        if (appType === 'rent') {
            appTypeCol = '<td>Аренда</td>'
        } else {
            appTypeCol = '<td>Продажа</td>'
        }

        var newRow = start + idCol + rowNumberCol + appTypeCol + propTypeCol + addressCol + priceCol + createdDateCol + viewCountCol + '</tr>';

        $('#publicApplicationsTable tbody').append(newRow);
    }

    function resetFilterInputs() {
        $('#filterForm input[name="price1"]').val("");
        $('#filterForm input[name="price2"]').val("");
        $('#filterForm input[name="city"]').val("");
        $('#filterForm input[name="street"]').val("");
    }
});