if ($('main.producer-orders').length > 0) {
    $('#changeOrderStatusBtn').click(function () {
        let change_status_btn = $('#changeOrderStatusBtn');
        $('#changeOrderStatusSelect').removeAttr('disabled');
        change_status_btn.css('display', 'none');
        $('#saveStatusOrderBtn').css('display', 'block');
    });

    function changeOrderStatus(order_id) {
        let order_status = {
            status: $('#changeOrderStatusSelect option:selected').val(),
        };
        $.ajax({
            url: "/api/v1/orders/" + order_id,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(order_status),
            success: function(data, status) {
                $('#saveStatusOrderBtn').css('display', 'none');
                $('#changeOrderStatusBtn').css('display', 'block');
                $('#changeOrderStatusSelect').attr('disabled', 'disabled');
            }
        });
    }

    $('#changeOrderStatusBtnTable').click(function () {
        let change_status_btn = $('#changeOrderStatusBtnTable');
        $('#changeOrderStatusSelectTable').removeAttr('disabled');
        change_status_btn.css('display', 'none');
        $('#saveStatusOrderBtnTable').css('display', 'block');
    });

    function changeOrderStatusTable(order_id) {
        let order_status = {
            status: $('#changeOrderStatusSelectTable option:selected').val(),
        };
        $.ajax({
            url: "/api/v1/orders/" + order_id,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(order_status),
            success: function(data, status) {
                $('#saveStatusOrderBtnTable').css('display', 'none');
                $('#changeOrderStatusBtnTable').css('display', 'block');
                $('#changeOrderStatusSelectTable').attr('disabled', 'disabled');
            }
        });
    }

}
