if ($('#producerProducts').length > 0) {
    // data for request
    var producer_sorts_and_filters = {
        price: null,
        popularity: null,
        category_name: null,
        producer_name: null,
        quantity: null,
        in_stock: 0
    };

    // get producer id
    let addr = window.location + '';
    addr = addr.split('/');
    var producer_id = addr[addr.length - 2];

    function getAndSetProducerName(producer_id) {
        $.get('/api/v1/producers/' + producer_id + '/name',
            function (data, status) {
                producer_sorts_and_filters['producer_name'] = data.producer_name;
            })
    }

    getAndSetProducerName(producer_id);

    // check what sorting option is selected
    function producer_fill_sorts_and_filters(producer_sorts_and_filters) {
        let selected_option_1 = $('#sortProducerProducts option:selected');
        if (selected_option_1.val() === 'По цене ↑') {
            producer_sorts_and_filters['popularity'] = null;
            producer_sorts_and_filters['price'] = 'up';
        }
        if (selected_option_1.val() === 'По цене ↓') {
            producer_sorts_and_filters['popularity'] = null;
            producer_sorts_and_filters['price'] = 'down';
        }
        if (selected_option_1.val() === 'По популярности') {
            producer_sorts_and_filters['popularity'] = 'down';
            producer_sorts_and_filters['price'] = null;
        }
    }

    function delete_current_producer_products() {
        var productSection = document.getElementById("producerProducts");
        while (productSection.firstChild) {
            productSection.removeChild(productSection.firstChild);
        }
    }

    function add_new_producer_products(products) {
        for (var i = 0; i < products.length; i++) {
            $("#producerProducts").append(
                '<div class="col-6 col-sm-3 card-item">' +
                '<a href="/products' + products[i].id + '">' +
                '<div class="product-item-photo">' +
                '<img src="\\' + products[i].photo_url + '"></div>' +
                '<div class="product-item-description" id="producerItemDescription' + i + '">' +
                "<p>" + products[i].price + "</p>" +
                "<b>" + products[i].name + "</b>" +
                '<p class="edit-product"><a href="/producer/' + producer_id + '/products/' + products[i].id + '/edit">' +
                "<img src='/static/img/edit-regular.svg'>Редактировать</a>" +
                "</p>" +
                "</div>" +
                "</a>" +
                "</div>");

            // if a product is out of stock, display a warning
            if (products[i].quantity === 0) {
                $("#producerItemDescription" + i).append(
                    '<p class="goods-ended">' +
                    '<img src= "/static/img/exclamation-circle-solid.svg">' +
                    'Нет в наличии' +
                    '</p>'
                )
            }
        }
    }

    function display_producer_filtered_and_sorted_products(producer_sorts_and_filters) {
        $.post('/api/v1/products/filter',
            producer_sorts_and_filters,
            function (products, status) {
                delete_current_producer_products();
                add_new_producer_products(products);
            });
    }


    function updateProducerProductsPage(producer_sorts_and_filters) {
        producer_fill_sorts_and_filters(producer_sorts_and_filters);
        display_producer_filtered_and_sorted_products(producer_sorts_and_filters);
    }

    $('#sortProducerProducts').change(function () {
        updateProducerProductsPage(producer_sorts_and_filters);
    });

    $('#in_stock').click(function () {
        if ($(this).is(":checked")) {
            producer_sorts_and_filters['in_stock'] = 1;
        } else {
            producer_sorts_and_filters['in_stock'] = 0;
        }
        updateProducerProductsPage(producer_sorts_and_filters);
    });
}