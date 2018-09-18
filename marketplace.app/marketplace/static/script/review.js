function makeReviewObject(consumer_name, consumer_id, product_id, body, order_id, rating) {
    return {
        consumer_name: consumer_name,
        consumer_id: parseInt(consumer_id),
        product_id: parseInt(product_id),
        order_id: order_id,
        body: body,
        rating: parseInt(rating)
    };
}

function postReview(data) {
    $.post('/api/v1/comments', data, function (response) {
        location.replace(window.location.origin + '/order_history/' + data.consumer_id);
    })
}


$('#sendReviews').click(function () {
    let newReviewSection = $('#newReviewSection');
    let consumer_name = newReviewSection.attr('data-consumer-name');
    let consumer_id = newReviewSection.attr('data-consumer-id');
    let order_id = newReviewSection.attr('data-order-id');
    let number_of_products = $(this).attr('data-number-of-products');

    for (let i = 1; i <= number_of_products; i++) {
        let review = $('#review' + i);
        let body = review.val();
        if (body) {
            let product_id = review.attr('data-product-id');
            for (let k = 1; k < 6; k++) {
                if ($('#ratingStar' + k + '_' + product_id).is(':checked')) {
                    var rating = k;
                    break;
                }

            }
            let data = makeReviewObject(consumer_name, consumer_id, product_id, body, order_id, rating);
            postReview(data);
        }
    }
});