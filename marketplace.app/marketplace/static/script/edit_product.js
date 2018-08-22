$(document).ready(function () {
    $('#editCategory').on('change', function () {
        $.get("/api/v1/categories/slug/" + this.value + "/subcategories/",
            function (data) {
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
            });
    });
});
