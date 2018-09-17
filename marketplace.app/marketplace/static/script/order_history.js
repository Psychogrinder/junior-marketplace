if ($('main.order-history').length > 0) {
    function cancelOrder(order_id) {
        $.ajax({
            url: '/api/v1/orders/' + order_id,
            type: 'DELETE',
            success: function (result) {
                $('#showOrderCancelModal').remove();
                $('.modal-backdrop').css("display", "none");
                $('.orders-block' + order_id).remove();
                $('body').removeClass('modal-open');
                var hulla = new hullabaloo();
                hulla.send("Заказ отменен", "secondary");
            }
        });
    }

    var order_data = {
        consumer_id: localStorage.getItem('globalUserId'),
        page: 1
    };

    let isInViewport = function (element) {
        let elementTop = element.offset().top;
        let elementBottom = elementTop + element.outerHeight();

        let viewportTop = $(window).scrollTop();
        let viewportBottom = viewportTop + $(window).height();

        return elementBottom > viewportTop && elementTop < viewportBottom;
    };

    $(window).on('resize scroll', function () {
        let element = $('.pageNumber');
        if (element.length > 0 && isInViewport(element)) {
            element.remove();
            order_data['page'] = element.attr("data-page-number");
            addOrders();
        }
    });

    function addOrders() {
        $.post("/api/v1/consumers/formatted_orders",
            order_data,
            function (data, status) {
                if (data.orders.length == 0) {
                    $('#consumerOrderHistory').append(
                        '<div class="container">' +
                        '<h3>У вас нет заказов</h3>' +
                        '</div>'
                    )
                }
                for (var i = 0; i < data.orders.length; i++) {
                    $('#consumerOrderHistory').append(
                        '<div class="orders-block' +
                        data.orders[i].id +
                        ' order-block-separator container">' +
                        '<div class="container">' +
                        '<div class="row order_history_info">' +
                        '<div class="col-2">' +
                        '<span>№ ' +
                        data.orders[i].id +
                        '</span>' +
                        '</div>' +
                        '<div class="col-4 order-history-producer-name">' +
                        '<a href="/producer/' +
                        data.orders[i].producer_id +
                        '" class="order-history-producer-link">' +
                        '<span>' +
                        data.orders[i].producer_name +
                        '</span>' +
                        '</a>' +
                        '</div>' +
                        '<div class="col-2 order_history_date"> ' +
                        '<span class="orderTimeStamp">' +
                        data.orders[i].placement_date +
                        '</span>' +
                        '</div>' +
                        '<div class="col-4"> ' +
                        '<span>СУММА ЗАКАЗА: ' +
                        data.orders[i].cost +
                        '</span>' +
                        '</div>' +
                        '</div>' +
                        '</div> ' +
                        '<div id="orderHistoryItemsContainer' +
                        data.orders[i].id +
                        '"></div>' +
                        '<div class="container delivery_container">' +
                        '<div class="row">' +
                        '<div class="col-3 delivery_value-header delivery_value">' +
                        '<span>Доставка:</span>' +
                        '</div>' +
                        '<div class="col-3 delivery_value">' +
                        '<span class="main-text">' +
                        data.orders[i].delivery_method +
                        '</span>' +
                        '</div>' +
                        '<div class="col-2">' +
                        '<span>Статус заказа:</span>' +
                        '</div>' +
                        '<div class="col-2">' +
                        '<span class="main-text">' +
                        data.orders[i].status +
                        '</span>' +
                        '</div>' +
                        '</div>' +
                        '<div id="orderButtonSection' +
                        data.orders[i].id +
                        '"></div>' +
                        '</div>' +
                        '<div class="modal fade" id="showOrderCancelModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">' +
                        '<div class="modal-dialog modal-min-dialog" role="document">' +
                        '<div class="modal-content">' +
                        '<div class="modal-header">' +
                        '<h5 class="modal-title" id="exampleModalLabel">Отмена заказа</h5>' +
                        '<button type="button" class="close" data-dismiss="modal" aria-label="Close">' +
                        '<span aria-hidden="true">&times;</span>' +
                        '</button>' +
                        '</div>' +
                        '<div class="modal-body">' +
                        '<p>Вы уверены, что хотите отменить заказ?</p>' +
                        '</div>' +
                        '<div class="modal-footer">' +
                        '<button type="button" class="btn btn-secondary" data-dismiss="modal">Закрыть</button>' +
                        '<button type="button" class="btn btn-primary" onclick="cancelOrder(' +
                        data.orders[i].id +
                        ')"> Отменить </button>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +
                        '</div>'
                    );
                    let items = data.orders[i].items;
                    for (let k = 0; k < items.length; k++) {
                        $('#orderHistoryItemsContainer' + data.orders[i].id).append(
                            '<div class="container order-history-product">' +
                            '<div class="row">' +
                            '<div class="col-2">' +
                            '<img class="order-product-photo" src="/' +
                            items[k].photo_url +
                            '" alt="" width="150px">' +
                            '</div>' +
                            '<div class="col-1 cart_product_stock_title">' +
                            '<p>Название</p>' +
                            '<p>Цена</p>' +
                            '<p>Артикул</p>' +
                            '</div>' +
                            '<div class="col-3 cart_product_stock_info">' +
                            '<a href="/products/' +
                             items[k].id +
                            '">' +
                            '<p>' +
                            items[k].name +
                            '</p>' +
                            '</a>' +
                            '<p>' +
                            items[k].price +
                            '</p>' +
                            '<p>#' +
                            items[k].id +
                            '</p>' +
                            '</div> <div class="col-2">' +
                            '<span>Вес:</span>' +
                            '<span class="main-text"> ' +
                            items[k].weight +
                            '</span>' +
                            '<span class="main-text"> ' +
                            items[k].measurement_unit +
                            '</span>' +
                            '</div>' +
                            '<div class="col-4 quantity_container">' +
                            '<span>Количество: </span>' +
                            '<span class="main-text">' +
                            items[k].quantity +
                            '</span>' +
                            '</div>' +
                            '</div>' +
                            '</div>'
                        )
                    }
                    if (data.orders[i].status === 'Не обработан') {
                        $('#orderButtonSection' + data.orders[i].id).append(
                            '<div class="row order-history-btn-block">' +
                            '<div class="col-4">' +
                            '<button class="btn btn-primary" type="button" data-toggle="modal" data-target="#showOrderCancelModal">' +
                            'ОТМЕНИТЬ ЗАКАЗ' +
                            '</button>' +
                            '</div>' +
                            '</div>'
                        )
                    } else if ((data.orders[i].status === 'Завершён') && (data.orders[i].reviewed !== true)) {
                        $('#orderButtonSection' + data.orders[i].id).append(
                            '<div class="row order-history-btn-block"> ' +
                            '<div class="col-4">' +
                            '<a href="/review/' +
                            data.orders[i].id +
                            '" class="btn btn-secondary">' +
                            'ОСТАВИТЬ ОТЗЫВ' +
                            '</a>' +
                            '</div> ' +
                            '</div>'
                        )
                    }



                    let next_page_number = data.page;
                    if (next_page_number) {
                        $("#consumerOrderHistory").append(
                            '<div data-page-number="' + next_page_number + '" class="pageNumber" style="width: 1px; height: 1px;" id="page' + next_page_number + '"></div>'
                        );
                    }
                }
            })
    }

    addOrders();
}

