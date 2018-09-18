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

function postReview(data, number_of_products, i) {
    $.post('/api/v1/comments', data, function () {
        i++;
        if (i <= number_of_products) {
            let newReviewSection = $('#newReviewSection');
            let consumer_name = newReviewSection.attr('data-consumer-name');
            let consumer_id = newReviewSection.attr('data-consumer-id');
            let order_id = newReviewSection.attr('data-order-id');
            let number_of_products = $(this).attr('data-number-of-products');
            sendReview(consumer_name, consumer_id, order_id, number_of_products, i)
        } else {
            location.replace(window.location.origin + '/order_history/' + data.consumer_id);
        }
    })
}

function sendReview(consumer_name, consumer_id, order_id, number_of_products, i) {
    let review = $('#review' + i);
    let body = review.val();
    let product_id = review.attr('data-product-id');
    for (let k = 1; k < 6; k++) {
        if ($('#ratingStar' + k + '_' + product_id).is(':checked')) {
            var rating = k;
            break;
        }
    }
    let data = makeReviewObject(consumer_name, consumer_id, product_id, body, order_id, rating);
    if (rating) {
        postReview(data, number_of_products, i);
    } else {
        var hulla = new hullabaloo();
        hulla.send("Вы забыли оценить товар", "danger");
    }
}

$('#sendReviews').click(function () {
    let newReviewSection = $('#newReviewSection');
    let consumer_name = newReviewSection.attr('data-consumer-name');
    let consumer_id = newReviewSection.attr('data-consumer-id');
    let order_id = newReviewSection.attr('data-order-id');
    let number_of_products = $(this).attr('data-number-of-products');
    let i = 1;
    sendReview(consumer_name, consumer_id, order_id, number_of_products, i)
});