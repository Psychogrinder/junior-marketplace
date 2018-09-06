function deleteProducerProduct(product_id) {
    $.ajax({
        url: '/api/v1/products/' + product_id,
        type: 'DELETE',
        success: function (result) {
            console.log(product_id);
            $('#deleteProductProducer').removeClass('show');
            $('#deleteProductProducer').css("display", "none");
            $('.modal-backdrop').css("display", "none");
            var user_id = localStorage.getItem("globalUserId");
            location.replace(window.location.origin + '/producer/' + user_id + '/products');
        }
    });
}