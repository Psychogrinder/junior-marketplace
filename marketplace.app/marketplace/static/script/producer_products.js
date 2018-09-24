if ($('#producerProducts').length > 0) {

    let isInViewport = function (element) {
        let elementTop = element.offset().top;
        let elementBottom = elementTop + element.outerHeight();

        let viewportTop = $(window).scrollTop();
        let viewportBottom = viewportTop + $(window).height();

        return elementBottom > viewportTop && elementTop < viewportBottom;
    };


    // фильтры, сортировка, поиск
    var producer_sorts_and_filters = {
        price: null,
        popularity: null,
        category_name: null,
        producer_name: null,
        quantity: null,
        search: null,
        in_stock: 0,
        page: 1
    };

    $(window).on('resize scroll', function () {
        let element = $('.pageNumber');
        // достигнув разделитель
        if (element.length > 0 && isInViewport(element)) {
            element.remove();
            producer_sorts_and_filters['page'] = element.attr("data-page-number");
            updateProducerProductsPage(producer_sorts_and_filters);
        }
    });

    // так как мы на странице производителя, мы сразу устанавливаем его имя в фильтр и больше не меняем его
    let addr = window.location + '';
    addr = addr.split('/');
    var producer_id = addr[addr.length - 2];

    function Initialize(producer_id) {
        $.get('/api/v1/producers/' + producer_id + '/name',
            function (data, status) {
                producer_sorts_and_filters['producer_name'] = data.producer_name;
                updateProducerProductsPage(producer_sorts_and_filters)
            })
    }

    // Initialize(producer_id);

    // наполняем объект параметрами: фильтры, сортировка, в наличии, поиск по имени
    function producer_fill_sorts_and_filters(producer_sorts_and_filters) {
        let selected_option_1 = $('#sortProducerProducts option:selected');
        if (selected_option_1.val() === 'По цене ↑') {
            producer_sorts_and_filters['popularity'] = null;
            producer_sorts_and_filters['rating'] = null;
            producer_sorts_and_filters['price'] = 'up';
        }
        if (selected_option_1.val() === 'По цене ↓') {
            producer_sorts_and_filters['popularity'] = null;
            producer_sorts_and_filters['rating'] = null;
            producer_sorts_and_filters['price'] = 'down';
        }
        if (selected_option_1.val() === 'По популярности') {
            producer_sorts_and_filters['popularity'] = 'down';
            producer_sorts_and_filters['rating'] = null;
            producer_sorts_and_filters['price'] = null
        }
        if (selected_option_1.val() === 'По рейтингу') {
            producer_sorts_and_filters['popularity'] = null;
            producer_sorts_and_filters['rating'] = 'down';
            producer_sorts_and_filters['price'] = null;
        }
        let searchKeyWord = $("#producerProductsSearch").val();
        if (searchKeyWord) {
            producer_sorts_and_filters['search'] = searchKeyWord;
        } else {
            producer_sorts_and_filters['search'] = null;
        }
    }

    function delete_current_producer_products() {
        var productSection = document.getElementById("producerProducts");
        while (productSection.firstChild) {
            productSection.removeChild(productSection.firstChild);
        }
    }

    function normalize_price(price) {
        let normalizePrice = price.split(' ');
        let priceArr = normalizePrice[0].split(' ');
        for (let i = 0; i < priceArr.length; i++) {
            priceArr[i] = Number(priceArr[i]);
        }
        priceArr = priceArr.join(' ');
        return priceArr + ' ₽';
    }

    function add_new_producer_products(products, next_page_number) {
        for (let i = 0; i < products.length; i++) {
            $("#producerProducts").append(
                '<div class="col-6 col-sm-3 card-item">' +
                '<a href="/products/' + products[i].id + '">' +
                '<div class="product-item-photo">' +
                '<img src="/' + products[i].photo_url + '"></div>' +
                '<div class="product-item-description" id="producerItemDescription' + products[i].id + '">' +
                "<p>" + normalize_price(products[i].price) + "</p>" +
                "<b>" + products[i].name + "</b>" +
                "</div>" +
                '<div class="product-rating product-rating--product-cart" id="productRating' +
                products[i].id +
                '">' +
                '</div>' +
                "</a>" +
                "</div>");

            // если продукта нет в наличии, отображаем предупреждение
            if (products[i].quantity === 0) {
                $("#producerItemDescription" + i).append(
                    '<p class="goods-ended">' +
                    '<img src= "/static/img/exclamation-circle-solid.svg">' +
                    'Нет в наличии' +
                    '</p>'
                )
            }

            if (localStorage.getItem("globalUserEntity") === 'producer') {
                $('#producerItemDescription' + products[i].id).append(
                    '<p class="edit-product"><a href="/producer/' + producer_id + '/products/' + products[i].id + '/edit">' +
                    "<img src='/static/img/edit-regular.svg'>Редактировать</a>" +
                    "</p>"
                );
            }

            for (let k = 0; k < products[i].stars.length; k++) {
                $('#productRating' + products[i].id).append(
                    '<span class="product-rating__icon">' +
                    '<img src="/static/' +
                    products[i].stars[k] +
                    '" alt="">' +
                    '</span>'
                )
            }

            $('#productRating' + products[i].id).append(
                '<span class="product-rating__number">' +
                products[i].rating +
                '</span>' +
                '<span class="product-rating__votes">' +
                '(' + products[i].votes + ')' +
                '</span>'
            );
        }

        // если есть следующая страница, то в конец прикрепляем разделитель, по достижении которого вновь
        // обновляем страницу
        if (next_page_number) {
            $("#producerProducts").append(
                '<div data-page-number="' + next_page_number + '" class="pageNumber" style="width: 1px; height: 1px;" id="page' + next_page_number + '"></div>'
            );
        }
    }

    function display_producer_filtered_and_sorted_products(producer_sorts_and_filters) {
        $.post('/api/v1/products/filter',
            producer_sorts_and_filters,
            function (products, status) {
                add_new_producer_products(products.products, products.next_page);
            });
    }


    function updateProducerProductsPage(producer_sorts_and_filters) {
        producer_fill_sorts_and_filters(producer_sorts_and_filters);
        display_producer_filtered_and_sorted_products(producer_sorts_and_filters);
    }

    $('#sortProducerProducts').change(function () {
        producer_sorts_and_filters['page'] = 1;
        delete_current_producer_products();
        updateProducerProductsPage(producer_sorts_and_filters);
    });

    $('#in_stock').click(function () {
        producer_sorts_and_filters['page'] = 1;
        delete_current_producer_products();
        if ($(this).is(":checked")) {
            producer_sorts_and_filters['in_stock'] = 1;
        } else {
            producer_sorts_and_filters['in_stock'] = 0;
        }
        updateProducerProductsPage(producer_sorts_and_filters);
    });

    $("#producerProductsSearch").on('keypress', function (e) {
        if (e.key === 'Enter') {
            // preventDefault() для того, чтобы по нажатию Enter в адресную строку не отправлялись параметры
            // нам это не нужно
            e.preventDefault();
            producer_sorts_and_filters['page'] = 1;
            delete_current_producer_products();
            updateProducerProductsPage(producer_sorts_and_filters);
        }
    });

    // Если не отображается надпись "У вас нет товаров", то устанавливаем имя производителя в фильтры и
    // запрашиваем первую страницу
    if ($('.producer_products_empty').length === 0) {
        Initialize(producer_id);

    }
}
