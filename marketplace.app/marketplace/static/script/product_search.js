//
// function getSearchResults(searchKeyWord) {
//     $.ajax({
//         url: "/search",
//         type: "get",
//         data: {
//             find: searchKeyWord,
//         },
//         success: function (products) {
//             // delete_current_producer_products();
//             // add_new_producer_products(products);
//             // console.log(products)
//         },
//         error: function (xhr) {
//             // console.log(xhr)
//         }
//     });
// }
//
//
// $("#globalSearch").on('keypress', function (e) {
//     if (e.key === 'Enter') {
//         getSearchResults($("#globalSearch").val())
//     }
// });