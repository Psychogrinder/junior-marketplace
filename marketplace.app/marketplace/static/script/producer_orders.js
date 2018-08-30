if ($('main.producer-orders').length > 0) {
    function changeOrderStatusBtn(order_id) {
        let change_status_btn = $('#changeOrderStatusBtn' + order_id);
        $('#changeOrderStatusSelect' + order_id).removeAttr('disabled');
        change_status_btn.css('display', 'none');
        $('#saveStatusOrderBtn' + order_id).css('display', 'block');
    }

    function changeOrderStatus(order_id) {
        let order_status = {
            status: $('#changeOrderStatusSelect' + order_id + ' option:selected').val(),
        };
        $.ajax({
            url: "/api/v1/orders/" + order_id,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(order_status),

            success: function (data, status) {
                $('#saveStatusOrderBtn' + order_id).css('display', 'none');
                $('#changeOrderStatusBtn' + order_id).css('display', 'block');
                $('#changeOrderStatusSelect' + order_id).attr('disabled', 'disabled');
                var hulla = new hullabaloo();
                hulla.send("Статус заказа изменен", "secondary");
            }
        });
    }

    $('#changeOrderStatusBtnTable').click(function () {

    });

    function changeOrderStatusBtnTable(order_id) {
        let change_status_btn = $('#changeOrderStatusBtnTable' + order_id);
        $('#changeOrderStatusSelectTable' + order_id).removeAttr('disabled');
        change_status_btn.css('display', 'none');
        $('#saveStatusOrderBtnTable' + order_id).css('display', 'block');
    }

    function changeOrderStatusTable(order_id) {
        let order_status = {
            status: $('#changeOrderStatusSelectTable' + order_id + ' option:selected').val(),
        };
        $.ajax({
            url: "/api/v1/orders/" + order_id,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(order_status),
            success: function (data, status) {
                $('#saveStatusOrderBtnTable'+order_id).css('display', 'none');
                $('#changeOrderStatusBtnTable'+order_id).css('display', 'block');
                $('#changeOrderStatusSelectTable'+order_id).attr('disabled', 'disabled');
                var hulla = new hullabaloo();
                hulla.send("Статус заказа изменен", "secondary");
            }
        });
    }

}
