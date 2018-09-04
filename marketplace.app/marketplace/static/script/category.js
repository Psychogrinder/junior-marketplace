$(document).ready(function () {
    if ($('#sortByPriceOrPopularity').length > 0) {
        // data for request
        var sorts_and_filters = {
            price: null,
            popularity: null,
            category_name: null,
            producer_name: null,
            quantity: null,
            in_stock: null
        };

        // get base category name
        var addr = window.location + '';
        addr = addr.split('/');
        var base_category = addr[addr.length - 1];


        $('.filter-block select').change(function () {
            update_page(sorts_and_filters, base_category);
        });

        $('#in_stock').change(function () {
            update_page(sorts_and_filters, base_category);
        });


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
                    delete_current_products();
                    add_new_products(products);
                    display_valid_options(sorts_and_filters, base_category)
                });
        }

        function delete_current_products() {
            var productSection = document.getElementById("productsByCategory");
            while (productSection.firstChild) {
                productSection.removeChild(productSection.firstChild);
            }
        }

        function add_new_products(products) {
            for (var i = 0; i < products.length; i++) {
                $("#productsByCategory").append(
                    '<div class="col-6 col-sm-3 card-item" >' +
                    "<a href='/products/" + products[i].id + "'>" +
                    '<div class="product-item-photo">' +
                    "<img src='/static/img/apple.jpg'>" +
                    "</div>" +
                    '<div class="product-item-description">' +
                    "<p>" + products[i].price + "</p>" +
                    "<b>" + products[i].name + "</b>" +
                    "<p>" + products[i].producer_name + "</p>" +
                    "</div>" +
                    "</a>" +
                    '</div>')
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

    }
});