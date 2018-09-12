function getComments(page_number) {
    let addr = window.location + '';
    addr = addr.split('/');
    let product_id = addr[addr.length - 1];

    $.ajax({
        url: "/api/v1/products/" + product_id + "/comments",
        data: {
            "page": page_number,
        },
        cache: false,
        type: "GET",
        success: function (response) {
            // add new comments to the comment section
            for (let comment in response.body) {
                comment = response.body[comment];

                $("#commentSection").append(
                    '<div class="review-product-item col-12 col-lg-9">' +
                    '<div class="row">' +
                    '<div class="col-12 col-sm-6">' +
                    '<p class="review-consumer">' + comment.consumer_name + '</p>' +
                    '</div>' +
                    '<div class="col-12 col-sm-6">' +
                    '<p class="review-data">' + comment.timestamp.split('T')[0] + '</p>' +
                    '</div>' +
                    '</div>' +
                    '<p class="review-comment">' + comment.body + '</p>' +
                    '</div>')
            }

            let currentPageNumber = response.meta.page;
            if (response.meta.has_next) {
                $("#commentsNextPage").prop("value", currentPageNumber + 1);
            } else {
                $("#commentsNextPage").hide();
            }
        },
    });
}

function updateCommentSection(page_number) {
    getComments(page_number);
}

$("#commentsNextPage").click(function () {
    updateCommentSection($(this).val())
});
