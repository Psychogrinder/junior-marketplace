// $(document).ready(function(){
//     $('#editCategory').on('change', function () {
//         alert("api/v1/categories/slug/" + this.value + "/subcategories/");
//     })
// });

$(document).ready(function () {
    $('#editCategory').on('change', function () {
        $.get("/api/v1/categories/slug/" + this.value + "/subcategories/",
            function (data) {
                var subcategories = data;

                var subcategory_option = $('.subcategory_option');
                if (subcategories.length > subcategory_option.length ) {

                }
                else if (subcategories.length < subcategory_option.length ) {

                }
                else {
                    console.log(subcategories);
                    for (var i = 0; i < subcategories.length; i++) {
                        subcategory_option[i].innerHTML = subcategories[i].name;
                        $(subcategory_option[i]).val(subcategories[i].slug);
                    }
                }
            });
    });
});
