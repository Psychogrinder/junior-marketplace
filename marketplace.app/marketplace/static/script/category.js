$(document).ready(function () {
        if ($('#sortByPriceOrPopularity').length > 0) {


            $(window).on('resize scroll', function () {
                let element = $('.pageNumber');
                if (element.length > 0 && isInViewport(element)) {
                    element.remove();
                    sorts_and_filters['page'] = element.attr("data-page-number");
                    update_page(sorts_and_filters, base_category);
                }
            });

            // data for request
            var sorts_and_filters = {
                price: null,
                popularity: null,
                category_name: null,
                producer_name: null,
                quantity: null,
                in_stock: 0,
                page: 1
            };

            // get base category name
            var addr = window.location + '';
            addr = addr.split('/');
            var base_category = addr[addr.length - 1];

            function fill_sorts_and_filters(sorts_and_filters, base_category) {
                let selected_option_1 = $('#sortByPriceOrPopularity option:selected');
                if (selected_option_1.val() === 'По цене ↑') {
                    sorts_and_filters['popularity'] = null;
                    sorts_and_filters['price'] = 'up';
                }
                if (selected_option_1.val() === 'По цене ↓') {
                    sorts_and_filters['popularity'] = null;
                    sorts_and_filters['price'] = 'down';
                }
                if (selected_option_1.val() === 'По популярности') {
                    sorts_and_filters['popularity'] = 'down';
                    sorts_and_filters['price'] = null
                }

                let selected_option_2 = $('#sortByCategory option:selected');
                if (selected_option_2.html() !== 'Подкатегория') {
                    sorts_and_filters['category_name'] = selected_option_2.html();
                } else {
                    sorts_and_filters['category_name'] = base_category;
                }

                let selected_option_3 = $('#sortByProducer option:selected');
                if (selected_option_3.html() !== 'Производитель') {
                    sorts_and_filters['producer_name'] = selected_option_3.html();
                } else {
                    sorts_and_filters['producer_name'] = null;
                }
            }

            function display_filtered_and_sorted_products(sorts_and_filters, base_category) {
                $.post('/api/v1/products/filter',
                    sorts_and_filters,
                    function (products, status) {
                        add_new_products(products.products, products.next_page);
                        display_valid_options(sorts_and_filters, base_category)
                    });
            }

            function delete_current_products() {
                var productSection = document.getElementById("productsByCategory");
                while (productSection.firstChild) {
                    productSection.removeChild(productSection.firstChild);
                }
            }

            function add_new_products(products, next_page_number) {
                for (var i = 0; i < products.length; i++) {
                    $("#productsByCategory").append(
                        '<div class="col-6 col-sm-3 card-item" >' +
                        '<a href="/products/' + products[i].id + '">' +
                        '<div class="product-item-photo">' +
                        '<img src="/' + products[i].photo_url + '"></div>' +
                        '<div class="product-item-description" id="categoryItemDescription' + i + '">' +
                        "<p>" + products[i].price + "</p>" +
                        "<b>" + products[i].name + "</b>" +
                        '<p class="producer_name">' + products[i].producer_name + "</p>" +
                        "</div>" +
                        "</a>" +
                        '</div>');
                    // if a product is out of stock, display a warning
                    if (products[i].quantity === 0) {
                        $("#categoryItemDescription" + i).append(
                            '<p class="goods-ended">' +
                            '<img src= "/static/img/exclamation-circle-solid.svg">' +
                            'Нет в наличии' +
                            '</p>');
                    }
                }
                if (next_page_number) {
                    $("#productsByCategory").append(
                        '<div data-page-number="' + next_page_number +  '" class="pageNumber" style="width: 1px; height: 1px;" id="page' + next_page_number + '"></div>'
                    );

                    // // let element = $('#page' + next_page_number);
                    // $(window).on('resize scroll', function (e) {
                    //     let element = document.getElementsByClassName('pageNumber')
                    //     if (element !== undefined && isInViewport(element)) {
                    //         console.log(element);
                    //         element.remove();
                    //         console.log(next_page_number);
                    //         sorts_and_filters['page'] = next_page_number;
                    //         update_page(sorts_and_filters, base_category);
                    //     }
                    // });
                }
            }

            function display_producers_that_have_the_selected_category(sorts_and_filters, base_category) {
                if (sorts_and_filters['category_name'] !== base_category) {
                    $.get('/api/v1/producers/' + sorts_and_filters['category_name'],
                        function (possible_producers, status) {
                            var producers = document.getElementById("sortByProducer");
                            for (let i = 1; i < producers.options.length; i++) {
                                if (possible_producers.indexOf(producers.options[i].value) > -1) {
                                    producers.options[i].style.display = 'block';
                                    if (sorts_and_filters['producer_name'] === producers.options[i]) {
                                        producers.options[i].attr("selected", "selected");
                                    }
                                } else {
                                    producers.options[i].style.display = 'none';
                                }
                            }
                        });
                } else {
                    var producers = document.getElementById("sortByProducer");
                    for (let i = 1; i < producers.options.length; i++) {
                        producers.options[i].style.display = 'block';
                    }
                }
            }

            function display_categories_that_the_selected_producer_has(sorts_and_filters, base_category) {
                if (sorts_and_filters['producer_name'] != null) {
                    $.get('/api/v1/categories/' + base_category + '/producer/' + sorts_and_filters['producer_name'],
                        function (possible_categories, status) {
                            var categories = document.getElementById("sortByCategory");
                            for (let i = 1; i < categories.options.length; i++) {
                                if (possible_categories.indexOf(categories.options[i].value) > -1) {
                                    categories.options[i].style.display = 'block';
                                    if (sorts_and_filters['category_name'] === categories.options[i]) {
                                        categories.options[i].attr("selected", "selected");
                                    }
                                } else {
                                    categories.options[i].style.display = 'none';
                                }
                            }
                        });
                } else {
                    var categories = document.getElementById("sortByCategory");
                    for (let i = 1; i < categories.options.length; i++) {
                        categories.options[i].style.display = 'block';
                    }
                }

            }

            function display_valid_options(sorts_and_filters, base_category) {
                display_producers_that_have_the_selected_category(sorts_and_filters, base_category);
                display_categories_that_the_selected_producer_has(sorts_and_filters, base_category);
            }

            function update_page(sorts_and_filters, base_category) {
                fill_sorts_and_filters(sorts_and_filters, base_category);
                display_filtered_and_sorted_products(sorts_and_filters, base_category);
            }

            $('.filter-block select').change(function () {
                delete_current_products();
                sorts_and_filters['page'] = 1;
                update_page(sorts_and_filters, base_category);
            });

            $('#in_stock_catalog_products').click(function () {
                delete_current_products();
                sorts_and_filters['page'] = 1;
                if ($(this).is(":checked")) {
                    sorts_and_filters['in_stock'] = 1;
                } else {
                    sorts_and_filters['in_stock'] = 0;
                }
                update_page(sorts_and_filters, base_category);
            });

            // добавляем товары на страницу при первой её загрзке
            update_page(sorts_and_filters, base_category);
        }

        let isInViewport = function (element) {
            let elementTop = element.offset().top;
            let elementBottom = elementTop + element.outerHeight();

            let viewportTop = $(window).scrollTop();
            let viewportBottom = viewportTop + $(window).height();

            return elementBottom > viewportTop && elementTop < viewportBottom;
        };
    }
);

