var getNumberOfUnprocessedOrders;
$(document).ready(function () {
    if ((localStorage.getItem("globalUserId") > 0) && (localStorage.getItem("globalUserEntity") === 'producer')) {

        var user_id = localStorage.getItem("globalUserId");
        getNumberOfUnprocessedOrders = function (user_id) {
            $.get("/api/v1/producers/" + user_id + "/unprocessed_orders",
                function (data, status) {
                    if (data.quantity) {
                        $('#producerOrders').append('<span class=\"badge badge-pill badge-secondary\">' + data.quantity + '</span>');
                    }
                });
        };
        getNumberOfUnprocessedOrders(user_id);
    }
});