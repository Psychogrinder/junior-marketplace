$(document).ready(function () {
    $("#emailRegProducer").change(function () {
        var email_producer = $("#emailRegProducer").val();
        var emailRegular = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
        if (!email_producer || (!(emailRegular.test(email_producer)))) {
            $('#emailRegProducer').css("border-color", "#FF7851");
        }
        else {
            $('#emailRegProducer').css("border-color", "#ced4da");
        }
    });


    $("#passwordRegProducer").change(function () {
        var password_producer = $("#passwordRegProducer").val();
        if (password_producer.length < 6) {
            $('#sixSymbolsRegProd').css("color", "#FF7851");
        }
        else {
            $('#sixSymbolsRegProd').css("color", "#888");
        }
    });


    $("#rePasswordRegProducer").change(function () {
        var re_password_producer = $("#rePasswordRegProducer").val();
        var password_producer = $("#passwordRegProducer").val();
        if (password_producer != re_password_producer) {
            $('#NonEqualPassword').css("display", "block");
        }
        else {
            $('#NonEqualPassword').css("display", "none");
        }
    });

    $('#nameRegProducer').change(function () {
        $('#nameRegProducer').css("border-color", "#ced4da");
    });


    $('#contactPersonRegProducer').change(function () {
        $('#contactPersonRegProducer').css("border-color", "#ced4da");
    });


    $('#phoneRegProducer').change(function () {
        $('#phoneRegProducer').css("border-color", "#ced4da");
    });


    $('#addressRegProducer').change(function () {
        $('#addressRegProducer').css("border-color", "#ced4da");
    });


    $("#registrationProducer").click(function () {
        var email_producer = $("#emailRegProducer").val();
        var password_producer = $("#passwordRegProducer").val();
        var re_password_producer = $("#rePasswordRegProducer").val();
        var name_producer = $("#nameRegProducer").val();
        var contact_producer = $("#contactPersonRegProducer").val();
        var phone_producer = $("#phoneRegProducer").val();
        var address_producer = $("#addressRegProducer").val();
        var description_producer = $("#descriptionRegProducer").val();
        console.log(phone_producer, address_producer, description_producer);
        var emailRegular = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;

        if (!email_producer || (!(emailRegular.test(email_producer)))) {
            $('#emailRegProducer').css("border-color", "#FF7851");
        }
        else if (password_producer.length < 6) {
            $('#sixSymbolsRegProd').css("color", "#FF7851");
        }
        else if (password_producer != re_password_producer) {
            $('#NonEqualPassword').css("display", "block");
        }
        else if (!name_producer) {
            $('#nameRegProducer').css("border-color", "#FF7851");
        }
        else if (!contact_producer) {
            $('#contactPersonRegProducer').css("border-color", "#FF7851");
        }
        else if (!phone_producer) {
            $('#phoneRegProducer').css("border-color", "#FF7851");
        }
        else if (!address_producer) {
            $('#addressRegProducer').css("border-color", "#FF7851");
        }
        else {
            $.post("/api/v1/producers",
                {
                    email: email_producer,
                    password: password_producer,
                    name: name_producer,
                    person_to_contact: contact_producer,
                    phone_number: phone_producer,
                    address: address_producer,
                    description: description_producer,
                },
                function (data, status) {
                    if (status == 'success') {
                        $('#regProducer').removeClass('show');
                        $('#regProducer').css("display", "none");
                        $('.modal-backdrop').css("display", "none");
                    }
                });
        }
    });
});