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
            success: function (data, status) {
                $('#saveStatusOrderBtn').css('display', 'none');
                $('#changeOrderStatusBtn').css('display', 'block');
                $('#changeOrderStatusSelect').attr('disabled', 'disabled');
                var hulla = new hullabaloo();
                hulla.send("Статус заказа изменен", "secondary");
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
            success: function (data, status) {
                $('#saveStatusOrderBtnTable').css('display', 'none');
                $('#changeOrderStatusBtnTable').css('display', 'block');
                $('#changeOrderStatusSelectTable').attr('disabled', 'disabled');
                var hulla = new hullabaloo();
                hulla.send("Статус заказа изменен", "secondary");
            }
        });
    }

    // data for request to get filtered orders
    let orderFilter = {
        producer_id: null,
        order_status: null,
    };

    // get and set producer id in orderFilter
    let addr = window.location + '';
    addr = addr.split('/');
    var producer_id = addr[addr.length - 2];
    orderFilter['producer_id'] = producer_id;

    function fill_order_filter(orderFilter) {
        orderFilter['order_status'] = $('#statuses option:selected').text();
    }

    function delete_current_orders() {
        let producerOrderSection = document.getElementById("producerOrderSection");
        while (producerOrderSection.firstChild) {
            producerOrderSection.removeChild(producerOrderSection.firstChild);
        }
    }

    function add_new_orders_common_view(orders) {
        for (var i = 0; i < orders.length; i++) {
            $("#producerOrderSection").append(
                '<div class="container item_order">' +
                '<div class="row order_history_info">' +
                '<div class="col-6">' +
                '<span>' + orders[i].id + '</span>' +
                '</div>' +
                '<div class="col-2">' + orders[i].order_timestamp + '</div>' +
                '<div class="col-3">' +
                '<span> СУММА ЗАКАЗА: ' + orders[i].total_cost + '</span>' +
                '</div>' +
                '</div>' +
                '<div id="orderProducts' + i + '"></div>' +
                '<div class="row">' +
                '<div class="col-6">' +
                '<div class="row producer-order-delivery">' +
                '<div class="col-4">Доставка:</div>' +
                '<div class="col-4 main-text">' + orders[i].delivery_method + '</div>' +
                '</div>' +
                '<div class="row producer-order-delivery">' +
                '<div class="col-4">Адрес:</div>' +
                '<div class="col-4 main-text">' + orders[i].delivery_address + '</div>' +
                '</div>' +
                '</div>' +
                '<div class="col-6">' +
                '<div class="row">' +
                '<div class="col-4">Покупатель:</div>' +
                '<div class="col-8 main-text">' + orders[i].first_name + ' ' + orders[i].last_name + '</div>' +
                '</div>' +
                '<div class="row">' +
                '<div class="col-4">Телефон:</div>' +
                '<div class="col-8 main-text">' + orders[i].consumer_phone + '</div>' +
                '</div>' +
                '<div class="row">' +
                '<div class="col-4">E-mail:</div>' +
                '<div class="col-8 main-text">' + orders[i].consumer_email + '</div>' +
                '</div>' +
                '<div class="row">' +
                '<div class="col-4">Статус заказа:</div>' +
                '<div class="col-8">' +
                '<select class="form-control select-order-status" disabled name="subcategory" id="changeOrderStatusSelect">' +
                '<option value="Обрабатывается">Все</option>' +
                '<option value="Обрабатывается">Не обработан</option>' +
                '<option value="Обрабатывается">Обрабатывается</option>' +
                '<option value="Обрабатывается">Отправлен</option>' +
                '<option value="Обрабатывается">Готов к самовывозу</option>' +
                '<option value="Обрабатывается">Завершён</option>' +
                '</select>' +
                '<button class="btn btn-warning common-view-btn" id="changeOrderStatusBtn">Изменить</button>' +
                '<button class="btn btn-success common-view-btn" id="saveStatusOrderBtn" onclick="changeOrderStatus(' + orders[i].id + ')">Сохранить' +
                '</button>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>'
            );
            var items = orders[i]['items'];
            for (var p = 0; p < items.length; p++) {
                $("#orderProducts" + i).append(
                    '<div class="row">' +
                    '<div class="col-2">' +
                    '<img class="order-product-photo" src="/static/img/apple-ant.jpg" alt="" width="150px">' +
                    '</div>' +
                    '<div class="col-4">' +
                    '<div class="row">' +
                    '<p class="col-6">Название</p>' +
                    '<p class="col-6 main-text">' + items[p].name + '</p>' +
                    '</div>' +
                    '<div class="row">' +
                    '<p class="col-6">Цена</p>' +
                    '<p class="col-6 main-text">' + items[p].price + '</p>' +
                    '</div>' +
                    '<div class="row">' +
                    '<p class="col-6">Артикул</p>' +
                    '<p class="col-6 main-text">' + items[p].id + '</p>' +
                    '</div>' +
                    '</div>' +
                    '<div class="col-2">' +
                    '<div class="row">' +
                    '<span class="col-6">Вес: </span>' +
                    '<span class="main-text col-6">' + items[p].weight + ' ' + items[p].measurement_unit + '</span>' +
                    '</div>' +
                    '</div>' +
                    '<div class="col-2">Количество:</div>' +
                    '<div class="col-1 main-text">' + items[p].quantity + '</div>' +
                    '</div>'
                )
            }
        }
    }

    function display_new_orders(orderFilter) {
        $.post('/api/v1/producers/filtered_orders',
            orderFilter,
            function (orders, status) {
                add_new_orders_common_view(orders);
            });
    }

    function add_event_listeners_to_buttons() {
        $('body').on('click', '#changeOrderStatusBtn', function () {
            let change_status_btn = $('#changeOrderStatusBtn');
            $('#changeOrderStatusSelect').removeAttr('disabled');
            change_status_btn.css('display', 'none');
            $('#saveStatusOrderBtn').css('display', 'block');
        });
        $('body').on('click', '#changeOrderStatusBtnTable', function () {
            let change_status_btn = $('#changeOrderStatusBtnTable');
            $('#changeOrderStatusSelectTable').removeAttr('disabled');
            change_status_btn.css('display', 'none');
            $('#saveStatusOrderBtnTable').css('display', 'block');
        });
    }


    function update_orders_page(orderFilter) {
        fill_order_filter(orderFilter);
        delete_current_orders();
        display_new_orders(orderFilter);
        add_event_listeners_to_buttons();
    }

    // update orders on change of the select
    $('#statuses').change(function () {
        console.log('IN select change');
        update_orders_page(orderFilter);
    });
}
