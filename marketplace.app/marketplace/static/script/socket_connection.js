namespace = '/chat';
if (localStorage.getItem("globalUserId")) {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
}

var current_date = null;
var entity = localStorage.getItem('globalUserEntity');
var orders_with_unread_messages = new Set();
socket.on('connect', function () {
    socket.emit('connected', {data: 'I\'m connected!'});
});

// ========== CHAT START ==========

function adjustHeaderMessageBadge() {
    $.get("/api/v1/chat/unread/" + localStorage.getItem("globalUserId"),
        function (numberOfMessages, status) {
            $('#numberOfUnreadMessagesBadge').html(numberOfMessages);
        });
}

function setUnreadMessagesToZero(id) {
    if (orders_with_unread_messages.has(id)) {
        orders_with_unread_messages.delete(id);
        // Удаляем бадж с кнопки "Связаться c..."
        let interlocutor;
        if (entity === 'producer') {
            $('#talkToConsumer' + id).html(' Связаться с покупателем ');
            interlocutor = 'consumer'
        } else if (entity === 'consumer') {
            $('#talkToProducer' + id).html(' Связаться с производителем ');
            interlocutor = 'producer'
        }
        // В данном случае entity - это человек, чьи сообщения были непрочитаны.
        $.post('/api/v1/chat',
            {
                order_id: id,
                entity: interlocutor
            },
            function (data) {
                adjustHeaderMessageBadge();
            })
    }
}

function appendMessage(data) {
    let chatWindow = $('#chat' + data['room']);
    // Если сообщения относятся к разным дням, то прикрепляем разделитель формата 02.07.2018
    let message_date = data.timestamp.split(' ')[1].split('.');
    // parseInt(message_date[1])-1 потому что Date принимает индекс месяца, а отсчёт начинается с нуля
    let new_date = new Date(parseInt(message_date[2]), parseInt(message_date[1]) - 1, parseInt(message_date[0]));
    if ((current_date - new_date) !== 0) {
        chatWindow.append(
            '<div class="date-divider">' + message_date[0] + "." + message_date[1] + "." + message_date[2] + '</div>'
        );
        current_date = new_date;
    }
    // прикрепляем сообщение
    chatWindow.append(
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
    // скроллим до дна окна с сообщениями
    chatWindow.scrollTop(1E10);
}

socket.on('response', function (data) {

    appendMessage(data);
// добавляем id заказа в нерпочитанные сообщения
    orders_with_unread_messages.add(data['room']);

// Если окно чата видно на экране, то сразу удаляем сообщение из непрочитанных. Если нет, то удалим по скроллу.
// Если нет, то удалим при следующем открытии чата.
    if (isInViewport($('#chat' + data['room']))) {
        setUnreadMessagesToZero(data['room'])
    }
});

function load_message_history(order_id) {
    $.get("/api/v1/chat/" + order_id,
        function (messages) {
            for (let i = 0; i < messages.length; i++) {
                appendMessage(messages[i]);
            }
            setUnreadMessagesToZero(order_id);
        })
}

function joinRoom(order_id) {
    socket.emit('join', {
        room: order_id
    });
    return false;
}

function startDialog(order_id) {
    if (entity === 'producer') {
        $('#talkToConsumer' + order_id).hide();
    } else if (entity === 'consumer') {
        $('#talkToProducer' + order_id).hide();
    }
    $("#orderDialog" + order_id).show();
    load_message_history(order_id);
    joinRoom(order_id);
}

function sendToRoom(order_id) {
    let inputField = $("#orderDialogMessage" + order_id);
    socket.emit('send_to_room', {
        room: order_id,
        body: inputField.val(),
        entity: entity
    });
    inputField.val('').focus()
}

// ========== CHAT  END ==========

// ========== ORDERS START ==========
socket.on('new_order_notification', function (data) {
    if (data['producer_id'] === localStorage.getItem('globalUserId')) {
        let order_badge = $('#numberOfNewOrders');
        order_badge.html(Number(order_badge.html()) + 1);
        let hulla = new hullabaloo();
        hulla.send("У вас новый заказ.", "secondary");
    }
});
// ========== ORDERS END ==========
