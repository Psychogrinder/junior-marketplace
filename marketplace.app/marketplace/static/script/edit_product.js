$(document).ready(function () {
    if ($('#editProductPage').length > 0) {

        var category_id;
        var parent_category_id;
        var addr = window.location + '';
        addr = addr.split('/');
        var product_id = addr[addr.length - 2];
        $.ajax({
            url: "/api/v1/products/" + product_id,
            success: handleChildCategory
        });

        $('#editPrice').inputmask("numeric", {
            radixPoint: ".",
            groupSeparator: " ",
            digits: 2,
            autoGroup: true,
            prefix: '',
            rightAlign: false
        });

        var productPrice = $('#editPrice').val();

        function formatPrice(x) {
            var strX = x.toString();
            var arr = strX.split(".");
            $('#editPrice').val(arr[0].split(" ").join(""));
        }

        formatPrice(productPrice);

        function fillMeasurements() {
            if (product.measurement_unit == 'кг') {
                $('#measurmentSelect').val('кг').attr('selected');
            } else if (product.measurement_unit == "шт") {
                $('#measurmentSelect').val('шт').attr('selected');
            } else {
                $('#measurmentSelect').val('л').attr('selected');
            }
            
        }

        function handleChildCategory(product_data) {
            var product = product_data;
            category_id = product.category_id;
            getParent(category_id)
        }

        function getParent(category_id) {
            $.ajax({
                url: "/api/v1/categories/" + category_id + "/parent",
                success: function (category_data) {
                    var parent_category = category_data;
                    parent_category_id = parent_category.id;
                    fillOptions(parent_category_id)
                }
            });
        }

        function fillOptions(parent_category_id) {
            $.ajax({
                url: "/api/v1/categories/base",
                success: function (data) {
                    for (var i = 0; i < data.length; i++) {
                        $("#editCategory").append('<option value="" class="category_option"></option>');
                    }
                    var category_option = $('.category_option');
                    for (var i = 0; i < data.length; i++) {
                        if (data[i].id == parent_category_id) {
                            category_option[i].innerHTML = data[i].name;
                            $(category_option[i]).val(data[i].slug);
                            var parent_slug = data[i].slug;
                            $(category_option[i]).attr('selected', true);
                        }
                        else {
                            category_option[i].innerHTML = data[i].name;
                            $(category_option[i]).val(data[i].slug);
                        }
                    }
                    getSubcategories(parent_slug)
                }
            });
        }

        function getSubcategories(parent_slug) {
            $.ajax({
                url: "/api/v1/categories/slug/" + parent_slug + "/subcategories/",
                success: function (data) {
                    var subcategories = data;
                    for (var i = 0; i < subcategories.length; i++) {
                        $('#editSubcategory').append('<option value="" class="subcategory_option"></option>')
                    }
                    var subcategory_option = $('.subcategory_option');
                    for (var i = 0; i < subcategories.length; i++) {
                        subcategory_option[i].innerHTML = subcategories[i].name;
                        $(subcategory_option[i]).val(subcategories[i].slug);
                        subcategory_option[i].setAttribute('data-id', subcategories[i].id);
                        if (subcategories[i].id == category_id) {
                            $(subcategory_option[i]).attr("selected", true);
                        }
                    }
                }});
        }

        $(document).ready(function () {
            $('#editCategory').on('change', function () {
                $.ajax({
                    url: "/api/v1/categories/slug/" + this.value + "/subcategories/",
                    success: function (data) {
                        var subcategories = data;
                        $('.subcategory_option').remove();
                        for (var i = 0; i < subcategories.length; i++) {
                            $('#editSubcategory').append('<option value="" class="subcategory_option"></option>')
                        }
                        var subcategory_option = $('.subcategory_option');
                        for (var i = 0; i < subcategories.length; i++) {
                            subcategory_option[i].innerHTML = subcategories[i].name;
                            $(subcategory_option[i]).val(subcategories[i].slug);
                        }
                    }});
            });
        });
    }
});
