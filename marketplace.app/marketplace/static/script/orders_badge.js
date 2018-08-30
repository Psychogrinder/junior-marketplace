var getNumberOfUnprocessedOrders;
if ((localStorage.getItem("globalUserId") > 0) && (localStorage.getItem("globalUserEntity") == 'producer')) {
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
        getNumberOfUnprocessedOrders(user_id);
    });