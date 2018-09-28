$(document).ready(function () {
    if ((localStorage.getItem("globalUserId") > 0) && (localStorage.getItem("globalUserEntity") === 'producer')) {
        let producer_id = localStorage.getItem("globalUserId");
        $.get("/api/v1/orders/new/" + producer_id,
            function (numberOfNewOrders, status) {
                $('#numberOfNewOrders').html(numberOfNewOrders);
            });
    }
});