$(document).ready(function () {
    var unitType = $('#createUnits option:selected').val();
    if (unitType != 'упаковка') {
        $('#createWeigth').css('display', 'none');
    }

    // var categoryId = null;

    $('#createProductSave').click(function(){
        // var addr = window.location + '';
        // addr = addr.split('/');
        // var product_id = addr[addr.length - 2];
        // var categorySlug = $('#editSubcategory option:selected').val();
        //
        // categoryId = parseInt($('#editSubcategory option:selected').data('id'));

        function createNewProductObject(){
            var newProductObject = {
                name: $('#createName').val(),
                price: $('#createPrice').val(),
                product_id: ,
                category_id: ,
                quantity: $('#createCount').val(),
                measurement_unit: $('#editUnits option:selected').val(),
                weight: $('#createWeigth').val(),
                description: $('#createDescription').html()
            };
            return newProductObject;
        }


        $.ajax({
            url: '/api/v1/products/' + product_id,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(newProductObject),
            success: function(data, status) {

            }
        });
    });
});
