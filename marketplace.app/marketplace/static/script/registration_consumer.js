$(document).ready(function () {
    $("#emailRegistration").change(function () {
        var email_registration = $("#emailRegistration").val();
        var emailRegular = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
        if (!email_registration || (!(emailRegular.test(email_registration)))) {
            $('#emailRegistration').css("border-color", "#FF7851");
        }
        else {
            $('#emailRegistration').css("border-color", "#ced4da");
        }
        $('#errorRegistrationConsumer').css('display', 'none');
    });

    $("#passwordRegistration").change(function () {
        var password_registration = $("#passwordRegistration").val();
        if (password_registration.length < 6) {
            $('#sixSimbolsAlert').css("color", "#FF7851");
        }
        else {
            $('#sixSimbolsAlert').css("color", "#888");
        }
    });

    $("#re_passwordRegistration").change(function () {
        var re_password_registration = $("#re_passwordRegistration").val();
        var password_registration = $("#passwordRegistration").val();
        if (password_registration != re_password_registration) {
            $('.invalid-feedback').css("display", "block");
        }
        else {
            $('.invalid-feedback').css("color", "#888");
        }
    });

    $("#reg_button").click(function () {
        var email_registration = $("#emailRegistration").val();
        var password_registration = $("#passwordRegistration").val();
        var re_password_registration = $("#re_passwordRegistration").val();
        var emailRegular = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
        if (!email_registration || (!(emailRegular.test(email_registration)))) {
            $('#emailRegistration').css("border-color", "#FF7851");
        }
        else if (password_registration.length < 6) {
            $('#sixSimbolsAlert').css("color", "#FF7851");
        }
        else if (password_registration != re_password_registration) {
            $('.invalid-feedback').css("display", "block");
        }
        else {
            $('main').css('display', 'none');
            $('#loadingSpinner').css('display', 'block');
            $('#singUpUser').removeClass('show');
            $('#singUpUser').css("display", "none");
            $('.modal-backdrop').css("display", "none");

            $.post("/api/v1/consumers",
                {
                    email: email_registration,
                    password: password_registration,
                },
                function (data, status) {
                    if (status) {
                        $.post("/api/v1/login",
                            {
                                email: email_registration,
                                password: password_registration,
                            },
                            function (data, status) {
                                if (status) {
                                    var globalUserId = data.id;
                                    localStorage.setItem("globalUserId", globalUserId);
                                    var globalUserEntity = data.entity;
                                    localStorage.setItem("globalUserEntity", globalUserEntity);
                                    location.reload();
                                }
                            });

                    }
                }).fail(function (data, textStatus, xhr) {
                if (data.status == 406) {
                    $('#errorRegistrationConsumer').css('display', 'block');
                    $('#errorRegistrationConsumer').text(data.responseJSON.message);
                }
            });
        }
    });
});
