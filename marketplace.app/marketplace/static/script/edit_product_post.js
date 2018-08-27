$(document).ready(function () {
    $('#save_product_data').click(function(){
        var addr = window.location + '';
        addr = addr.split('/');
        var product_id = addr[addr.length - 2];
        var categorySlug = $('#editSubcategory option:selected').val();

        $.get('/api/v1/categories/' + categorySlug,
            function (data, status) {
                if (status) {
                    createProductObject(data);
                }
        });

        function createProductObject(categoryId){
            var productObject = {
                name: $('#editName').val(),
                price: $('#editPrice').val(),
                category_id: categoryId,
                quantity: $('#editCount').val(),
                weight: $('#editWeigth').val(),
                measurement_unit: $('#editUnits option:selected').val(),
                description: $('#editDescription').html()
            };
            // console.log(productObject);
            return productObject;
        }

        console.log(createProductObject(product_id));

        $.ajax({
            url: '/api/v1/products/' + product_id,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(createProductObject(product_id)),
            success: function(data, status) {
                // console.log(data, status);
            }
        });
    });
});
