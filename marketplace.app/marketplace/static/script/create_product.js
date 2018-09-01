$(document).ready(function () {
    if ($('main .edit-product-card').length > 0) {

        var categoryId;
        var default_category_id = 1;
        var addr = window.location + '';
        addr = addr.split('/');
        var producerId = addr[addr.length - 2];

        function createNewProductObject(){
            categoryId = parseInt($('#createSubcategory option:selected').data('id'));
            var obj = {
                name: $('#createName').val(),
                price: $('#createPrice').val(),
                producer_id: producerId,
                category_id: categoryId,
                quantity: $('#createCount').val(),
                measurement_unit: $('#createUnits option:selected').val(),
                weight: $('#createWeigth').val()
            };
            return obj;
        }

        function fillOptions(category_id) {
            $.ajax({
                url: "/api/v1/categories/base",
                success: function (data) {
                    for (var i = 0; i < data.length; i++) {
                        $("#createCategory").append('<option value="" class="category_option"></option>');
                    }

                    var category_option = $('.category_option');
                    for (var i = 0; i < data.length; i++) {
                        if (data[i].id == category_id) {
                            var parent_slug = data[i].slug;
                        }
                        category_option[i].innerHTML = data[i].name;
                        $(category_option[i]).val(data[i].slug);
                    }
                    getSubcategories(parent_slug)
                }
            });
        }

        function getSubcategories(parent_slug) {
            $.get("/api/v1/categories/slug/" + parent_slug + "/subcategories/",
                function (data) {
                    var subcategories = data;
                    for (var i = 0; i < subcategories.length; i++) {
                        $('#createSubcategory').append('<option value="" class="subcategory_option"></option>')
                    }
                    var subcategory_option = $('.subcategory_option');
                    for (var i = 0; i < subcategories.length; i++) {
                        subcategory_option[i].innerHTML = subcategories[i].name;
                        $(subcategory_option[i]).val(subcategories[i].slug);
                        subcategory_option[i].setAttribute('data-id', subcategories[i].id);
                    }
                });
        }

        function createProduct () {
            var newProductObject = createNewProductObject();

            $.ajax({
                url: '/api/v1/products',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(newProductObject),
                success: function(data, status) {
                    location.replace('/products/' + data.id);
                }
            });
        }

        fillOptions(default_category_id);

        $('#createCategory').on('change', function () {
            $.get("/api/v1/categories/slug/" + this.value + "/subcategories/",
                function (data) {
                    var subcategories = data;
                    $('.subcategory_option').remove();
                    for (var i = 0; i < subcategories.length; i++) {
                        $('#createSubcategory').append('<option value="" class="subcategory_option"></option>')
                    }
                    var subcategory_option = $('.subcategory_option');
                    for (var i = 0; i < subcategories.length; i++) {
                        subcategory_option[i].innerHTML = subcategories[i].name;
                        $(subcategory_option[i]).val(subcategories[i].slug);
                        subcategory_option[i].setAttribute('data-id', subcategories[i].id);
                    }
                });
        });

        $('#createProductForm').submit(function(e) {
            e.preventDefault();
            createProduct();
        });
    }
});
