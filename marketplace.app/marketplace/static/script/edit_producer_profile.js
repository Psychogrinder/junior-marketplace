$(document).ready(function () {
    $(".phone_mask").mask("+7(999)999-99-99");

    $('#save_producer_profile').click(function(){
        var addr = window.location + '';
        addr = addr.split('/');
        var producer_id = addr[addr.length - 2];
        var producerObject = {
            name: $('#producer_name').val(),
            person_to_contact: $('#producer_contact_person').val(),
            email: $('#producer_email').val(),
            // fileHelp: $('#producer_logo').val(),
            phone: $('#producer_phone').val(),
            address: $('#producer_adress').val(),
            description: $('#producer_description').val()
        };
        
        $.ajax({
            url: '/api/v1/producers/' + producer_id,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(producerObject),
            success: function(data, status) {
<<<<<<< HEAD
                var hulla = new hullabaloo();
                hulla.send("Профиль успешно изменен", "secondary");
=======

>>>>>>> f87728aa55e77a01611bccf0cf985c096dce890f
            }
        });
    });
});
