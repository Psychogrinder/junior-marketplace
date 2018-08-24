$(document).ready(function () {
    // if ($('main .edit-profile').length > 0) {
    //     // var consumer;
        // var addr = window.location + '';
        // addr = addr.split('/');
        // var consumer_id = addr[addr.length - 1];
        // $.ajax({
        //     url: "/api/v1/users/" + consumer_id,
        //     success: function (consumer_data) {
        //         console.log(consumer_data);
        //     }
    //     // });
    // }

    $('#save_consumer_profile').click(function(){
        var addr = window.location + '';
        addr = addr.split('/');
        var consumer_id = addr[addr.length - 1];
        var consumerObject = {
            email: $('#consumer_email').val(),
            first_name: $('#consumer_first_name').val(),
            last_name: $('#consumer_last_name').val(),
            phone_number: $('#consumer_phone').val(),
            address: $('#consumer_adress').val(),
            patronymic: $('#consumer_patronymic').val()
        };
        $.ajax({
            url: '/api/v1/consumers/' + consumer_id,
            type: 'PUT',
            data: JSON.stringify(consumerObject),
            dataType: 'json',
            success: function(data, status) {
                alert(data, status);
            }
        });
    });
});
