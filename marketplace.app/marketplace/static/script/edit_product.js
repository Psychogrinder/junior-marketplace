// $(document).ready(function () {
//     $('#editCategory').on('change', function () {
//         $.get("/api/v1/categories/slug/" + this.value + "/subcategories/",
//             function (data) {
//                 var subcategories = data;
//                 $('.subcategory_option').remove();
//                 for (var i = 0; i < subcategories.length; i++) {
//                     $('#editSubcategory').append('<option value="" class="subcategory_option"></option>')
//                 }
//                 var subcategory_option = $('.subcategory_option');
//                 for (var i = 0; i < subcategories.length; i++) {
//                     subcategory_option[i].innerHTML = subcategories[i].name;
//                     $(subcategory_option[i]).val(subcategories[i].slug);
//                 }
//             });
//     });
// });


$(document).ready(function () {
    var category_id ;
    var parent_category_id;

    if ($('main .edit-product-card').length > 0) {

        var addr = window.location + '';
        addr = addr.split('/');
        var product_id = addr[addr.length-2];
        $.ajax({
            url: "/api/v1/products/" + product_id,
            success: handleChildCategory
        });

        function handleChildCategory(product_data) {
            var product = product_data;
            category_id = product.category_id;
            console.log("got", category_id);
            getParent(category_id)
        }

        function getParent(category_id) {
            $.ajax({
                url: "/api/v1/categories/" + category_id + "/parent",
                success: function (category_data) {
                    var parent_category = category_data;
                    parent_category_id = parent_category.id;
                    console.log("parent " + parent_category_id);
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
                        console.log(data[i].id, parent_category_id, data[i].name);
                        if (data[i].id == parent_category_id) {
                            console.log("TRUE");
                            category_option[i].innerHTML = data[i].name;
                            $(category_option[i]).val(data[i].slug);
                            // $(category_option[i]).selected = "selected";
                            // $(category_option[i]).selected = "true";
                            // $(category_option[i]).selected = true;
                            var slug = data[i].slug;
                            $("#editCategory option[value=]").prop('selected', true);
                            console.log("ALSO TRUE");
                        }
                        else {
                            category_option[i].innerHTML = data[i].name;
                            $(category_option[i]).val(data[i].slug);
                        }
                    }
                }
            });
        }

    //     $.get("/api/v1/categories/slug/" + this.value + "/subcategories/",
    //         function (data) {
    //             var subcategories = data;
    //             $('.subcategory_option').remove();
    //             for (var i = 0; i < subcategories.length; i++) {
    //                 $('#editSubcategory').append('<option value="" class="subcategory_option"></option>')
    //             }
    //             var subcategory_option = $('.subcategory_option');
    //             for (var i = 0; i < subcategories.length; i++) {
    //                 subcategory_option[i].innerHTML = subcategories[i].name;
    //                 $(subcategory_option[i]).val(subcategories[i].slug);
    //             }
    //         });
    //
    }
});
