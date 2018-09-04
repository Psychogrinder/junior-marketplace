$(document).ready(function () {
    var categoryId = null;

    function uploadProductImage(product_id) {
        var form_data = new FormData($('#upload-product-image')[0]);
        $.ajax({
            type: 'POST',
            url: "/api/v1/products/" + product_id + "/upload",
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                console.log('Success!');
            },
        });
    }

    $('#save_product_data').click(function () {
        var addr = window.location + '';
        addr = addr.split('/');
        var product_id = addr[addr.length - 2];
        var categorySlug = $('#editSubcategory option:selected').val();

        categoryId = parseInt($('#editSubcategory option:selected').data('id'));

        function createProductObject(categoryId) {
            var productObject = {
                name: $('#editName').val(),
                price: $('#editPrice').val(),
                category_id: categoryId,
                quantity: $('#editCount').val(),
                weight: $('#editWeigth').val(),
                measurement_unit: $('#editUnits option:selected').val(),
                description: $('#editDescription').html()
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
    });
});
