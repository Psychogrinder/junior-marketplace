if ($('main.order-history').length > 0) {
    function cancelOrder(order_id) {
        $.ajax({
            url: '/api/v1/orders/' + order_id,
            type: 'DELETE',
            success: function (result) {
                $('#showOrderCancelModal').remove();
                $('.modal-backdrop').css("display", "none");
                $('.orders-block'+order_id).remove();
                $('body').removeClass('modal-open');
            }
        });
    }
}