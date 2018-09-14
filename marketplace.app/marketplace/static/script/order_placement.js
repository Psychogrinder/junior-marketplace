if ($('main .order_registration').length > 0) {
    countTotalCost();
    $("#orderPlacementBtn").click(function () {
        let firstName = $('#orderRegistrationFirstName').val();
        let lastName = $('#orderRegistrationLastName').val();
        let email = $('#orderRegistrationEmail').val();
        let phone = $('#orderRegistrationPhone').val();
        let address = $('#orderRegistrationAddress').val();
        let producer_ids = $('.visuallyHiddenProducerId').text();
        producer_ids.split('');
        let orders = [];
        for (let i = 0; i < producer_ids.length; i++) {
            let producer_block = $(".registration-order-items" + producer_ids[i]);
            let delivery = producer_block.find('.deliveryMethodSelect option:selected').val();
            orders[i] = {
                producer_id: producer_ids[i],
                delivery_method: delivery,
            };
        }
        for (let i = 0; i < orders.length; i++) {
            if (orders[i].delivery_method == 'Курьером') {
                checkAddressField();
            }
        }

        function checkAddressField() {
            $("#orderRegistrationFirstAddress").css("border-color", "#FF7851");
        }

        if (!email) {
            $("#orderRegistrationEmail").css("border-color", "#FF7851");
        }
        else if (!phone) {
            $("#orderRegistrationPhone").css("border-color", "#FF7851");
        }
        else {
            var user_id = localStorage.getItem("globalUserId");
            $.post("/api/v1/orders",
                {
                    consumer_id: user_id,
                    first_name: firstName,
                    last_name: lastName,
                    email: email,
                    phone: phone,
                    delivery_address: address,
                    orders: JSON.stringify(orders),
                },
                function (data, status) {
                    if (status) {
                        $('.order_registration').remove();
                        $('#numberOfProductsInCart').remove();
                        $('main').append('<section class="container total_container py-4" id="emptyCart">\n' +
                            '                 <h2>Ваш заказ был успешно оформлен. С Вами свяжутся в ближайшее время. </h2>\n' +
                            '            </section>')
                    }
                }).fail(function (data, textStatus, xhr) {
                    if (data.status == 406) {
                        var hulla = new hullabaloo();
                        hulla.send(data.responseJSON.message, "secondary");
                    }
                });
        }
    });
}
