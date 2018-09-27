var number_of_products_in_cart = 0;
var putToCart = function (consumer_id, product_id) {
    if ($(".product_quantity_input").val() > 0) {
        $.post("/api/v1/consumers/" + consumer_id + "/cart",
            {
                product_id: product_id,
                quantity: $(".product_quantity_input").val(),
                mode: 'inc'
            },
            function (data, status) {
                number_of_products_in_cart = 0;
                for (var k in data.items) {
                    if (data.items.hasOwnProperty(k)) {
                        number_of_products_in_cart += parseInt(data.items[k]);
                    }
                }
                document.getElementById('numberOfProductsInCart').innerHTML = number_of_products_in_cart;
                var hulla = new hullabaloo();
                hulla.send("Товар успешно добавлен в корзину", "default");

            });
    }
};

if ($('.product-card-main').length > 0) {
    $('.product_quantity_input').on('change keyup input click mouseup', function () {
        if (this.value.match(/[^0-9]|^0{1}/g)) {
            this.value = this.value.replace(/./g, '');
        }
        let products_in_stock = $('#allProductsInStock').text();
        let product_quantity = $('.product_quantity_input').val();
        if (product_quantity > Number(products_in_stock)) {
            $('.product_quantity_input').val(products_in_stock);
        }
    });
    $('.product_quantity_input').on('change', function () {
        let product_quantity = $('.product_quantity_input').val();
        if (product_quantity == '' || product_quantity < 1) {
            $('.product_quantity_input').val(1);
        }
    });
}

var getNumberOfProductsInCart;
if ((localStorage.getItem("globalUserId") > 0) && (localStorage.getItem("globalUserEntity") == 'consumer')) {
    $(document).ready(function () {
        var user_id = localStorage.getItem("globalUserId");
        getNumberOfProductsInCart = function (user_id) {
            $.get("/api/v1/consumers/" + user_id + "/cart/quantity",
                function (data, status) {
                    if (data.number_of_products) {
                        document.getElementById('numberOfProductsInCart').innerHTML = data.number_of_products;
                    }
                });
        };
        getNumberOfProductsInCart(user_id);
    });
}


function deleteProduct(product_id, consumer_id) {
    $('#' + product_id).remove();
    $.post("/api/v1/consumers/" + consumer_id + "/cart",
        {
            product_id: product_id,
            mode: 'remove'
        },
        function (data, status) {
            number_of_products_in_cart = 0;
            for (var k in data.items) {
                if (data.items.hasOwnProperty(k)) {
                    number_of_products_in_cart += parseInt(data.items[k]);
                }
            }
            document.getElementById('numberOfProductsInCart').innerHTML = number_of_products_in_cart;
            $('.notEmptyCart').find('.' + product_id).remove();

        });

    var allProductBlock = $('.notEmptyCart section');
    console.log(allProductBlock.length);
    if (allProductBlock.length == 1) {
        $('.notEmptyCart').remove();
        $('#cartMain').append('<section class="container total_container py-4" id="emptyCart">\n' +
            '                 <h2>Ваша корзина пуста</h2>\n' +
            '            </section>')
    }
    countTotalCost();

}

function getProductsByUserId() {
    var user_id = localStorage.getItem("globalUserId");
    if ((localStorage.getItem("globalUserId") > 0) && (localStorage.getItem("globalUserEntity") == 'consumer')) {
        $.get("/api/v1/products/" + user_id + "/cart",
            function (products, status) {
                if (status) {
                    getCartInformation(products);
                }
            }
        )
    }
}

function getCartInformation(products) {
    var user_id = localStorage.getItem("globalUserId");
    $.get("/api/v1/consumers/" + user_id + "/cart",
        function (items, status) {
            if (status) {
                countTotalCostInner(items, products);
            }
        })
}

function countTotalCostInner(items, products) {
    var total = 0;
    for (var i in items.items) {
        for (var p = 0; p < products.length; p++) {
            if (i == products[p].id) {
                var sum = items.items[i] * products[p].price.substring(0, products[p].price.length - 1);
                total += sum;
            }
        }
    }
    $('#totalCost').html(total);
}

function countTotalCost() {
    getProductsByUserId();
}

if (localStorage.getItem("globalUserId") > 0) {
    countTotalCost();
}

function changeQuantityOfProduct(product_id) {
    let quantity = $('#number' + product_id).val();
    if ($('#cartMain').length > 0) {
        if (quantity == '' || quantity < 1) {
            quantity = 1;
        }
        if (Number(quantity) > Number($('#allProductsInStock' + product_id).text())) {
            quantity = Number($('#allProductsInStock' + product_id).text());
            console.log('more');
        }
    }
    $('#number' + product_id).val(quantity);
    var user_id = localStorage.getItem("globalUserId");
    $.post("/api/v1/consumers/" + user_id + "/cart",
        {
            product_id: product_id,
            quantity: quantity,
            mode: 'set'
        },
        function (data, status) {
            number_of_products_in_cart = 0;
            for (var k in data.items) {
                if (data.items.hasOwnProperty(k)) {
                    number_of_products_in_cart += parseInt(data.items[k]);
                }
            }
            document.getElementById('numberOfProductsInCart').innerHTML = number_of_products_in_cart;
        });
    countTotalCost();
}


//при загрузке страницы проверяем наличие товара в корзине
if ($('#cartMain').length > 0) {
    let products_in_stock = $('[id^=allProductsInStock]');
    let input_value = $('.product_quantity_input');
    for (let i = 0; i < products_in_stock.length; i++) {
        if (Number($(products_in_stock[i]).text()) < $(input_value[i]).val()) {
            $(input_value[i]).val(Number($(products_in_stock[i]).text()));
            var user_id = localStorage.getItem("globalUserId");
            let product_id = parseInt(/[0-9]+/.exec($(products_in_stock[i]).attr('id')));
            changeQuantityOfProduct(product_id);
        }
        if (Number($(products_in_stock[i]).text()) == 0) {
            let cssValues = {
                'background-color': 'rgba(0, 0, 0, 0.03)',
                'border-radius': '5px',
                'margin-bottom': '2rem',
                'padding-top': '1rem'
            };
            $(input_value[i]).css('border-color', '#ee686e');
            let product_id = parseInt(/[0-9]+/.exec($(products_in_stock[i]).attr('id')));
            $('#productCartItemAlert' + product_id).css(cssValues);
            $('#alertProductOutOfStock' + product_id).css('display', 'block');
        }
    }

}
