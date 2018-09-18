$(document).ready(function () {
    $('#save_consumer_profile').click(function(){
        var addr = window.location + '';
        addr = addr.split('/');
        var consumer_id = addr[addr.length - 1];
        var consumerObject = {
            first_name: $('#consumer_first_name').val(),
            last_name: $('#consumer_last_name').val(),
            phone_number: $('#consumer_phone').val(),
            address: $('#consumer_address').val(),
            patronymic: $('#consumer_patronymic').val()
        };
        $.ajax({
            url: '/api/v1/consumers/' + consumer_id,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(consumerObject),
            success: function(data, status) {
                if ($('.parsley-error').length == 0) {
                    location.replace('/user/' + consumer_id);
                }
            }
        });
    });
});
