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

    // ===============================   AJAX   ===============================

    let currentOrders;

    // data for request to get filtered orders
    let orderFilter = {
        producer_id: null,
        order_status: null,
        page: 1,
    };

    let isInViewport = function (element) {
        let elementTop = element.offset().top;
        let elementBottom = elementTop + element.outerHeight();

        let viewportTop = $(window).scrollTop();
        let viewportBottom = viewportTop + $(window).height();

        return elementBottom > viewportTop && elementTop < viewportBottom;
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
        let producerOrderSectionTable = document.getElementById("producerOrderSectionTable");
        while (producerOrderSectionTable.firstChild) {
            producerOrderSectionTable.removeChild(producerOrderSectionTable.firstChild);
        }
    }

    function add_new_orders_common_view(orders, page) {
        for (var i = 0; i < orders.length; i++) {
            $("#producerOrderSection").append(
                '<div class="container item_order">' +
                '<div class="row order_history_info">' +
                '<div class="col-6">' +
                '<span>№ </span>' +
                '<span id="orderId' + i + '">' + orders[i].id + '</span>' +
                '</div>' +
                '<div class="col-2">' + orders[i].order_timestamp + '</div>' +
                '<div class="col-3">' +
                '<span> СУММА ЗАКАЗА: ' + orders[i].total_cost + '</span>' +
                '</div>' +
                '</div>' +
                '<div id="orderProducts' + orders[i].id + '"></div>' +
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
                '<select class="form-control select-order-status" name="subcategory" id="changeOrderStatusSelect' + i + '" onchange="orderStatusOnChange(' + i + ')">' +
                '<option value="Не обработан">Не обработан</option>' +
                '<option value="Обрабатывается">Обрабатывается</option>' +
                '<option value="Отправлен">Отправлен</option>' +
                '<option value="Готов к самовывозу">Готов к самовывозу</option>' +
                '<option value="Завершён">Завершён</option>' +
                '</select>' +
                '<button class="btn btn-success common-view-btn save-status-order-btn" id="saveStatusOrderBtn' + i + '" onclick="saveOrderStatusClicked(' + i + ')">Сохранить</button>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>'
            );
            let items = orders[i]['items'];
            for (let p = 0; p < items.length; p++) {
                $("#orderProducts" + orders[i].id).append(
                    '<div class="row">' +
                    '<div class="col-2">' +
                    '<img class="order-product-photo" src="/' + items[p].photo_url + '" alt="" width="150px">' +
                    '</div>' +
                    '<div class="col-4">' +
                    '<div class="row">' +
                    '<p class="col-6">Название</p>' +
                    '<a href="/products/' + items[p].id + '">' +
                    '<p class="col-12 main-text">' + items[p].name + '</p>' +
                    '</a>' +
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
        let next_page_number = page;
        if (next_page_number) {
            $("#producerOrderSection").append(
                '<div style="width: 1px; height: 1px;" id="page' + next_page_number + '"></div>'
            );

            let element = $('#page' + next_page_number);
            $(window).on('resize scroll', function () {
                if (isInViewport(element)) {
                    element.remove();
                    orderFilter['page'] = next_page_number;
                    update_orders_page(orderFilter);
                }
            });
        }
    }

    function add_new_orders_table_view(orders, page) {
        for (var i = 0; i < orders.length; i++) {
            $("#producerOrderSectionTable").append(
                '<div class="container table_container hidden">' +
                '<div class="table_global_row">' +
                '<div class="table_global_cell">' +
                '<div>Номер заказа</div>' +
                '<div class="main-text" id="orderIdTable' + i + '">' + orders[i].id + '</div>' +
                '</div>' +
                '<div class="table_global_cell">' +
                '<div>Покупатель</div>' +
                '<div class="main-text">' + orders[i].first_name + ' ' + orders[i].last_name + '</div>' +
                '</div>' +
                '<div class="table_global_cell">' +
                '<div>Телефон</div>' +
                '<div class="main-text">' + orders[i].consumer_phone + '</div>' +
                '</div>' +
                '<div class="table_global_cell">' +
                '<div>E-mail</div>' +
                '<div class="main-text">' + orders[i].consumer_email + '</div>' +
                '</div>' +
                '<div class="table_global_cell">' +
                '<div>Дата заказа</div>' +
                '<div class="main-text">' + orders[i].order_timestamp + '</div>' +
                '</div>' +
                '</div>' +
                '<div class="table_global_row">' +
                '<div class="table_global_cell">' +
                '<div>Товар</div>' +
                '</div>' +
                '<div class="table_global_cell">' +
                '<div>Цена</div>' +
                '</div>' +
                '<div class="table_global_cell">' +
                '<div>Артикул</div>' +
                '</div>' +
                '<div class="table_global_cell">' +
                '<div>Количество</div>' +
                '</div>' +
                '</div>' +
                '<div id="innerTableProductsSection' + orders[i].id + '"></div>' +
                '<div class="table_global_row">' +
                '<div class="table_global_cell">' +
                '<div>Способ доставки</div>' +
                '<div class="main-text">' + orders[i].delivery_method + '</div>' +
                '</div>' +
                '<div class="table_global_cell">' +
                '<div>Адрес</div>' +
                '<div class="main-text">' + orders[i].delivery_address + '</div>' +
                '</div>' +
                '<div class="table_global_cell">' +
                '<div>Сумма заказа</div>' +
                '<div class="main-text">' + orders[i].total_cost + '</div>' +
                '</div>' +
                '<div class="table_global_cell">' +
                '<div>Статус заказа</div>' +
                '<select class="form-control select-order-status" id="changeOrderStatusSelectTable' + i + '" name="subcategory" onchange="orderStatusOnChange(' + i + ')">' +
                '<option value="Не обработан">Не обработан</option>' +
                '<option value="Обрабатывается">Обрабатывается</option>' +
                '<option value="Отправлен">Отправлен</option>' +
                '<option value="Готов к самовывозу">Готов к самовывозу</option>' +
                '<option value="Завершён">Завершён</option>' +
                '</select>' +
                '</div>' +
                '<div class="table_global_cell">' +
                '<button class="btn btn-success common-view-btn save-status-order-btn" id="saveStatusOrderBtnTable' + i + '" onclick="saveOrderStatusClicked(' + i + ')">Сохранить</button>' +
                '</div>' +
                '</div>' +
                '</div>'
            );
            let items = orders[i]['items'];
            for (let p = 0; p < items.length; p++) {
                $("#innerTableProductsSection" + orders[i].id).append(
                    '<div class="table_global_row">' +
                    '<div class="table_global_cell producer-orders-item">' +
                    '<div class="main-text">' + items[p].name + '</div>' +
                    '</div>' +
                    '<div class="table_global_cell producer-orders-item">' +
                    '<div class="main-text">' + items[p].price + items[p].weight + items[p].measurement_unit + '</div>' +
                    '</div>' +
                    '<div class="table_global_cell producer-orders-item">' +
                    '<div class="main-text">' + items[p].id + '</div>' +
                    '</div>' +
                    '<div class="table_global_cell producer-orders-item">' +
                    '<div class="main-text">' + items[p].quantity + '</div>' +
                    '</div>' +
                    '</div>'
                );
            }
        }
        let next_page_number = page;
        if (next_page_number) {
            $("#producerOrderSectionTable").append(
                '<div style="width: 1px; height: 1px;" id="tablePage' + next_page_number + '"></div>'
            );

            let element = $('#tablePage' + next_page_number);
            $(window).on('resize scroll', function () {
                if (isInViewport(element)) {
                    element.remove();
                    orderFilter['page'] = next_page_number;
                    update_orders_page(orderFilter);
                }
            });
        }
    }

    // Set the right status of each order
    function set_selected_options() {
        for (let i = 0; i < currentOrders.length; i++) {
            let currentSelect = document.getElementById('changeOrderStatusSelect' + i);
            for (var o = 0; o < currentSelect.options.length; o++) {
                if (currentSelect.options[o].value === currentOrders[i].status) {
                    currentSelect.options[o].selected = 'selected'
                }
            }
            let currentSelectTable = document.getElementById('changeOrderStatusSelectTable' + i);
            for (var o = 0; o < currentSelectTable.options.length; o++) {
                if (currentSelectTable.options[o].value === currentOrders[i].status) {
                    currentSelectTable.options[o].selected = 'selected'
                }
            }
        }
    }

    // if a different order status is selected, show "save" button
    function orderStatusOnChange(i) {
        if (currentOrdersView === 'common') {
            $('#saveStatusOrderBtn' + i).show();
        } else if (currentOrdersView === 'table') {
            $('#saveStatusOrderBtnTable' + i).show();
        }
    }


    function changeOrderStatusInDB(order_id, order_status, i) {
        $.ajax({
            url: "/api/v1/orders/" + order_id,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify({status: order_status}),
            success: function (data, status) {
                // hide "save" buttons until a different status is selected
                $('#saveStatusOrderBtn' + i).hide();
                $('#saveStatusOrderBtnTable' + i).hide();
                var hulla = new hullabaloo();
                hulla.send("Статус заказа изменен", "secondary");
            }
        })
    }

    // on click of "save" button: get the new selected status, order id and send a request
    function saveOrderStatusClicked(i) {
        if (currentOrdersView === 'common') {
            var select = document.getElementById("changeOrderStatusSelect" + i);
            var order_status = select.options[select.selectedIndex].value;
            var order_id = document.getElementById("orderId" + i).innerHTML;
            changeOrderStatusInDB(order_id, order_status, i)
        } else if (currentOrdersView === 'table') {
            var select = document.getElementById("changeOrderStatusSelectTable" + i);
            var order_status = select.options[select.selectedIndex].value;
            var order_id = document.getElementById("orderIdTable" + i).innerHTML;
            changeOrderStatusInDB(order_id, order_status, i)
        }

    }


    function display_new_orders(orderFilter) {
        $.post('/api/v1/producers/filtered_orders',
            orderFilter,
            function (orders, status) {
                currentOrders = orders.orders;
                add_new_orders_common_view(orders.orders, orders.page);
                add_new_orders_table_view(orders.orders, orders.page);
                set_selected_options();
                if (currentOrdersView === 'table') {
                    $('#page' + orders.page).hide();
                    showTable()
                } else {
                    currentOrdersView = 'common';
                    $('#tablePage' + orders.page).hide();
                    showCommon();
                }

                // hide all "save" buttons until a new status is selected
                for (var i = 0; i < orders.orders.length; i++) {
                    $("#saveStatusOrderBtn" + i).hide();
                    $("#saveStatusOrderBtnTable" + i).hide();
                }
            });
    }


    function update_orders_page(orderFilter) {
        fill_order_filter(orderFilter);
        display_new_orders(orderFilter);
    }


// update orders on change of the main select
    $('#statuses').change(function () {
        delete_current_orders();
        orderFilter['page'] = 1;
        update_orders_page(orderFilter);
    });
    update_orders_page(orderFilter);
}
