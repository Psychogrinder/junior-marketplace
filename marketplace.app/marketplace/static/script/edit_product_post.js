$(document).ready(function () {
    var categoryId = null;


    function uploadProductImage(product_id) {
        console.log("IN UPLOAD");
        var image_data = $('#item-img-output').attr('src');
        image_data = image_data.split(',')[1];
        // var form_data = new FormData($('#upload-producer-image')[0]);
        $.ajax({
            type: 'POST',
            url: "/api/v1/products/" + product_id + "/upload",
            data: {
                image_data: image_data,
            },
            success: function (data, status) {
                console.log('successful upload');
            },
        });
    }

    $('#save_product_data').click(function (event) {
        event.preventDefault();
        var addr = window.location + '';
        addr = addr.split('/');
        var product_id = addr[addr.length - 2];
        var categorySlug = $('#editSubcategory option:selected').val();

        categoryId = parseInt($('#editSubcategory option:selected').data('id'));

        function createProductObject(categoryId) {
            var productObject = {
                name: $('#editName').val(),
                price: $('#editPrice').val(),
                category_id: $('#editSubcategory').val(),
                quantity: $('#editCount').val(),
                weight: $('#editWeight').val(),
                measurement_unit: $('#editUnits option:selected').val(),
                description: $('#editDescription').val()
            };
            return productObject;
        }

        $.ajax({
            url: '/api/v1/products/' + product_id,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(createProductObject(categoryId)),
            success: function (data, status) {
                uploadProductImage(product_id);

            }
        });
        var hulla = new hullabaloo();
        hulla.send("Информация о товаре сохранена", "secondary");
    });
});
