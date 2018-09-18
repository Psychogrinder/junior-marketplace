$(document).ready(function () {
    var categoryId = null;

    function uploadProductImage(product_id) {
        var image_data = $('#item-img-output').attr('src');
        image_data = image_data.split(',')[1];
        $.ajax({
            type: 'POST',
            url: "/api/v1/products/" + product_id + "/upload",
            data: {
                image_data: image_data,
            },
            success: function (data, status) {

            },
        });
    }

    $('#save_product_data').click(function () {
        function submitEditProductForm(){
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
                    measurement_unit: $('#measurmentSelect option:selected').val(),
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
        }



        $('#editProductForm').submit(function (event) {
            event.preventDefault();
            submitEditProductForm();
        });
    });
});
