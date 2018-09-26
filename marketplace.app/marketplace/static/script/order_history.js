if ($('main.order-history').length > 0) {

    // ========= Chat functionality start =========
    var current_date = null;
    var orders_with_unread_messages = new Set();
    // Use a "/test" namespace.
    // An application can open a connection on multiple namespaces, and
    // Socket.IO will multiplex all those connections on a single
    // physical channel. If you don't care about multiple channels, you
    // can set the namespace to an empty string.
    namespace = '/chat';
    // Connect to the Socket.IO server.
    // The connection URL has the following format:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    // Event handler for new connections.
    // The callback function is invoked when a connection with the
    // server is established.
    socket.on('connect', function () {
        socket.emit('connected', {data: 'I\'m connected!'});
    });


    function appendMessage(data) {
        // Если сообщения относятся к разным дням, то прикрепляем разделитель формата 02.07.2018
        let message_date = data.timestamp.split(' ')[1].split('.');
        let day = parseInt(message_date[0]);
        let month = parseInt(message_date[1]);
        let year = parseInt(message_date[2]);
        // month-1 потому что Date принимает индекс месяца, а отсчёт начинается с нуля
        let new_date = new Date(year, month - 1, day);
        if ((current_date - new_date) !== 0) {
            $('#chat' + data['room']).append(
                '<div>' + day + "." + month + "." + year + '</div>'
            );
            current_date = new_date;
        }
        // прикрепляем сообщение
        $('#chat' + data['room']).append(
            '<div class="order-dialog__item">' +
            '<div class="row order-dialog__header">' +
            '<div class="col-4 col-sm-2 order-dialog__photo">' +
            '<img src="/' + data['photo_url'] + '" alt="">' +
            '</div>' +
            '<div class="col-8 col-sm-7 order-dialog__name">' +
            '<p class="main-text">' + data['username'] + '</p>' +
            '<p class="main-text">' + data['body'] + '</p>' +
            '</div>' +
            '<div class="col-8 col-sm-3 order-dialog__date">' +
            '<p>' + data['timestamp'].split(' ')[0] + '</p>' +
            '</div>' +
            '</div>' +
            '</div>'
        );

    }

    socket.on('response', function (data) {
        console.log('GOT A RESPONSE start');
        console.log(data);
        console.log('GOT A RESPONSE end');
        appendMessage(data);
    });

    function load_message_history(order_id) {
        $.get("/api/v1/chat/" + order_id,
            function (data) {
                console.log(data);
                for (let i = 0; i < data.length; i++) {
                    appendMessage(data[i]);
                }
            })
    }

    function joinRoom(order_id) {
        socket.emit('join', {
            room: order_id
        });
        return false;
    }

    function startDialog(order_id) {
        $("#orderDialog" + order_id).show();
        $("#connectCustomer" + order_id).css('display', 'none');
        load_message_history(order_id);
        joinRoom(order_id);
    }

    function sendToRoom(order_id) {
        let inputField = $("#orderDialogMessage" + order_id);
        socket.emit('send_to_room', {
            room: order_id,
            body: inputField.val(),
            entity: 'consumer'
        });
        inputField.val('').focus()
    }

    // ========= Chat functionality end =========


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

        for (let id of orders_with_unread_messages.keys()) {
            let lastElement = $('#chat' + id + ' div:last-child');
            if (lastElement.length > 0) {
                if (isInViewport(lastElement)) {
                    console.log('YAY');
                    // В данном случае entity - это человек, чьи сообщения были непрочитаны.
                    $.post('/api/v1/chat',
                        {
                            order_id: id,
                            entity: 'producer'
                        },
                        function (data) {
                            console.log
                        })
                }
            }
        }

    });

    function addOrders() {
        $.post("/api/v1/consumers/formatted_orders",
            order_data,
            function (data, status) {
                if (data.orders.length === 0) {
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
                        // first row start
                        '<div class="row order_history_info">' +
                        '<div class="col-12 col-lg-2">' +
                        '<span>№ ' +
                        data.orders[i].id +
                        '</span>' +
                        '</div>' +
                        '<div class="col-12 col-lg-4 order-history-producer-name">' +
                        '<a href="/producer/' +
                        data.orders[i].producer_id +
                        '" class="order-history-producer-link">' +
                        '<span>' +
                        data.orders[i].producer_name +
                        '</span>' +
                        '</a>' +
                        '</div>' +
                        '<div class="col-12 col-lg-2 order_history_date"> ' +
                        '<span class="orderTimeStamp">' +
                        data.orders[i].placement_date +
                        '</span>' +
                        '</div>' +
                        '<div class="col-12 col-lg-4"> ' +
                        '<span>СУММА ЗАКАЗА: ' +
                        data.orders[i].cost +
                        '</span>' +
                        '</div>' +
                        '</div>' +
                        '</div> ' +
                        // first row finish
                        '<div id="orderHistoryItemsContainer' +
                        data.orders[i].id +
                        '"></div>' +
                        '<div class="container delivery_container">' +
                        // third row start
                        '<div class="row">' +
                        '<div class="col-5 col-lg-2 delivery_value-header delivery_value">' +
                        '<span>Доставка:</span>' +
                        '</div>' +
                        '<div class="col-7 col-lg-3 delivery_value">' +
                        '<span class="main-text">' +
                        data.orders[i].delivery_method +
                        '</span>' +
                        '</div>' +
                        '<div class="col-5 col-lg-2">' +
                        '<span>Статус заказа:</span>' +
                        '</div>' +
                        '<div class="col-7 col-lg-3">' +
                        '<span class="main-text">' +
                        data.orders[i].status +
                        '</span>' +
                        '</div>' +
                        '</div>' +
                        // third row finish
                        '<div class="order-buttons-section" id="orderButtonSection' +
                        data.orders[i].id +
                        '">' +
                        '<button type="button" class="btn btn-primary" id="connectCustomer' +
                        data.orders[i].id +
                        '" onclick="startDialog(' +
                        data.orders[i].id +
                        ')"> Связаться с производителем </button>' +
                        '</div>' +
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

                        // chat window interface start
                        '<section class="container order-dialog" id="orderDialog' + data.orders[i].id + '">' +
                        '<div class="message-history" id="chat' + data.orders[i].id + '">' +
                        '</div>' +
                        '<div class="order-dialog__form col-12 col-lg-10">' +
                        '<textarea type="text" class="form-control" rows="4" id="orderDialogMessage' + data.orders[i].id + '" name="orderDialogMessage">' +
                        '</textarea>' +
                        '<div class="order-dialog__btn-block">' +
                        '<button class="btn btn-secondary" onclick="sendToRoom(' + data.orders[i].id + ')">Отправить</button>' +
                        '</div>' +
                        '</div>' +
                        '</section>' +
                        // chat window interface end
                        '</div>'
                    );
                    let items = data.orders[i].items;
                    for (let k = 0; k < items.length; k++) {
                        $('#orderHistoryItemsContainer' + data.orders[i].id).append(
                            // second row start
                            '<div class="container order-history-product">' +
                            '<div class="row">' +
                            '<div class="col-12 col-lg-2">' +
                            '<img class="order-product-photo" src="/' +
                            items[k].photo_url +
                            '" alt="" width="150px">' +
                            '</div>' +
                            '<div class="col-5 col-lg-1 cart_product_stock_title">' +
                            '<p>Название</p>' +
                            '<p>Цена</p>' +
                            '<p>Артикул</p>' +
                            '</div>' +
                            '<div class="col-7 col-lg-3 cart_product_stock_info">' +
                            '<a href="/products/' +
                            items[k].id +
                            '">' +
                            '<p>' +
                            items[k].name +
                            '</p>' +
                            '</a>' +
                            '<p>' +
                            items[k].price + ' / ' + items[k].measurement_unit +
                            '</p>' +
                            '<p>#' +
                            items[k].id +
                            '</p>' +
                            '</div>' +
                            '<div class="col-7 col-lg-4 px-lg-0 quantity_container">' +
                            '<span>Количество: </span>' +
                            '<span class="main-text">' +
                            items[k].quantity +
                            '</span>' +
                            '</div>' +
                            '</div>' +
                            '</div>'
                            // second row finish
                        )
                    }

                    if (data.orders[i].status === 'Не обработан') {
                        $('#orderButtonSection' + data.orders[i].id).append(
                            '<div class="order-history-btn-block">' +
                            '<div class="col-12-right">' +
                            '<button class="btn btn-danger btn-order-history-cancel" type="button" data-toggle="modal" data-target="#showOrderCancelModal">' +
                            'ОТМЕНИТЬ ЗАКАЗ' +
                            '</button>' +
                            '</div>' +
                            '</div>'
                        )
                    } else if ((data.orders[i].status === 'Завершён') && (data.orders[i].reviewed !== true)) {
                        $('#orderButtonSection' + data.orders[i].id).append(
                            '<div class="order-history-btn-block"> ' +
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
                    // Это нужно для того, чтобы отправлять запросы для определённых заказов, а не всех.
                    if (data.orders[i].has_unread_messages) {
                        orders_with_unread_messages.add(data.orders[i].id);
                    }
                }
                let next_page_number = data.page;
                if (next_page_number) {
                    $("#consumerOrderHistory").append(
                        '<div data-page-number="' + next_page_number + '" class="pageNumber" style="width: 1px; height: 1px;" id="page' + next_page_number + '"></div>'
                    );
                }
            })
    }

    addOrders();
}
