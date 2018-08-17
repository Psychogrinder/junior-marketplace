// function increaseValue() {
//   var value = parseInt(document.getElementById('number').value, 10);
//   value = isNaN(value) ? 0 : value;
//   value++;
//   document.getElementById('number').value = value;
// }
//
// function decreaseValue() {
//   var value = parseInt(document.getElementById('number').value, 10);
//   value = isNaN(value) ? 0 : value;
//   value < 1 ? value = 1 : '';
//   value--;
//   document.getElementById('number').value = value;
// }

function increaseQuantity(id) {
  var value = parseInt(document.getElementById(id).value, 10);
  value = isNaN(value) ? 0 : value;
  value++;
  document.getElementById(id).value = value;
}

function decreaseQuantity(id) {
  var value = parseInt(document.getElementById(id).value, 10);
  value = isNaN(value) ? 0 : value;
  value < 1 ? value = 1 : '';
  value--;
  document.getElementById(id).value = value;
}
