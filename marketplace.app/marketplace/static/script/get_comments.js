// function clearCommentSection() {
//     let myNode = document.getElementById("commentSection");
//     while (myNode.firstChild) {
//         myNode.removeChild(myNode.firstChild);
//     }
// }

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
                    '<div>' +
                    '<hr>' +
                    '<p>' + comment.consumer_name + '</p>' +
                    '<p>' + comment.timestamp.split('T')[0] + '</p>' +
                    '<p>' + comment.body + '</p>' +
                    '<hr>' +
                    '</div>')
            }

            // display previous page and next page buttons
            let currentPageNumber = response.meta.page;
            if (response.meta.has_next) {
                $("#commentsNextPage").prop("value", currentPageNumber + 1);
            } else {
                $("#commentsNextPage").hide();
            }


        },
        error: function (xhr) {
            console.log(xhr)
        }
    });
}

function updateCommentSection(page_number) {
    // clearCommentSection();
    getComments(page_number)
}

$("#commentsNextPage").click(function () {
    updateCommentSection($(this).val())
});

$("#commentsPrevPage").click(function () {
    updateCommentSection($(this).val())
});