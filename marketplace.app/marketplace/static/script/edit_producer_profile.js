$(document).ready(function () {

    $(".phone_mask").mask("+7(999)999-99-99");

    function uploadProducerImage(producer_id) {
        var form_data = new FormData($('#upload-producer-image')[0]);
        $.ajax({
            type: 'POST',
            url: "/api/v1/producers/" + producer_id + "/upload",
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function (photo_url) {
                if (photo_url) {
                    document.getElementById("upload-producer-image").reset();
                    var imageDiv = document.getElementById("editProducerImage");
                    while (imageDiv.firstChild) {
                        imageDiv.removeChild(imageDiv.firstChild);
                    }
                    $("#editProducerImage").append(
                        '<img src="' + photo_url + '" alt="" width="100%" height="auto">'
                    );
                }
            },
        });
    }


    $('#save_producer_profile').click(function () {
        var producerObject = {
            name: $('#producer_name').val(),
            person_to_contact: $('#producer_contact_person').val(),
            // email: $('#producer_email').val(),
            // fileHelp: $('#producer_logo').val(),
            phone_number: $('#producer_phone').val(),
            address: $('#producer_address').val(),
            description: $('#producer_description').val()
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
                    hulla.send("Профиль успешно изменен", "secondary");
                    uploadProducerImage(producer_id);
                }
            });
        };

        $('#editProducerForm').submit(function (event) {
            event.preventDefault();
            submitEditProfileForm();

        });
    })
    ;
});
