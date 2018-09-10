//
// function getSearchResults(searchKeyWord) {
//     $.ajax({
//         url: "/api/v1/products/search",
//         type: "get",
//         data: {
//             find: searchKeyWord,
//         },
//         success: function (products) {
//             delete_current_producer_products();
//             add_new_producer_products(products);
//             console.log(products)
//         },
//         error: function (xhr) {
//             console.log(xhr)
//         }
//     });
// }


// $("#producerProductsSearch").on('keypress', function (e) {
//     if (e.key === 'Enter') {
//         getSearchResults($("#producerProductsSearch").val())
//     }
// });