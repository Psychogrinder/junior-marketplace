var number_of_products_in_cart = 0;
var putToCart = function (consumer_id, product_id) {
    console.log(consumer_id, product_id);
    $.post("/api/v1/consumers/" + consumer_id + "/cart",
        {
            product_id: product_id,
            quantity: $(".product_quantity_input").val()
        },
        function (data, status) {
            number_of_products_in_cart = 0;
            for (var k in data.items) {
                if (data.items.hasOwnProperty(k)) {
                    number_of_products_in_cart += parseInt(data.items[k]);
                }
            }
            document.getElementById('numberOfProductsInCart').innerHTML = number_of_products_in_cart;
            console.log(number_of_products_in_cart);
        });
};

var getNumberOfProductsInCart;
$(document).ready(function () {
    var user_id = localStorage.getItem("globalUserId");
    getNumberOfProductsInCart = function (user_id) {
        $.get("/api/v1/consumers/" + user_id + "/cart/quantity",
            function (data, status) {
                console.log("data.number_of_products: " + data.number_of_products);
                if (data.number_of_products) {
                    document.getElementById('numberOfProductsInCart').innerHTML = data.number_of_products;
                }
            });
    };
    getNumberOfProductsInCart(user_id);
});



