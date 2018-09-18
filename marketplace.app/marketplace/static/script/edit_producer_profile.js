$(document).ready(function () {

    $(".phone_mask").mask("+7(999)999-99-99");

    function uploadProducerImage(producer_id) {
        var image_data = $('#item-img-output').attr('src');
        image_data = image_data.split(',')[1];
        $.ajax({
            type: 'POST',
            url: "/api/v1/producers/" + producer_id + "/upload",
            data: {
                image_data: image_data,
            },
            success: function (data, status) {

            },
        });
    }


    $('#save_producer_profile').click(function () {
        var producerObject = {
            name: $('#producer_name').val(),
            person_to_contact: $('#producer_contact_person').val(),
            phone_number: $('#producer_phone').val(),
            address: $('#producer_address').val(),
            description: description_textarea.value()
        };

        function submitEditProfileForm() {
            var addr = window.location + '';
            addr = addr.split('/');
            var producer_id = addr[addr.length - 2];
            $.ajax({
                url: '/api/v1/producers/' + producer_id,
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(producerObject),
                success: function (data, status) {
                    var hulla = new hullabaloo();
                    hulla.send("Профиль успешно изменен", "default");
                    uploadProducerImage(producer_id);
                }
            });
        };

        $('#editProducerForm').submit(function (event) {
            event.preventDefault();
            submitEditProfileForm();
        });
    });

    // Если на странице есть поле для редактирования описания производителя, то преобразуем его в редактор
    if ($("#producer_description").length > 0) {
        var description_textarea = new SimpleMDE({element: document.getElementById("producer_description")});
    }
});
