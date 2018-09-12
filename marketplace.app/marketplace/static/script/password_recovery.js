$('#passwordRecovery').click(function () {
    var email = $('#emailResetPassword').val();
    var emailRegular = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
    if (!email || (!(emailRegular.test(email)))) {
        $("#emailResetPassword").css("border-color", "#FF7851");
    } else {
        $.post("/api/v1/password/recovery",
            {
                email: email,
            },
            function (data, status) {
                if (status) {
                    $('#resetPasssword').removeClass('show');
                    $('#resetPasssword').css("display", "none");
                    $('.modal-backdrop').css("display", "none");
                    var hulla = new hullabaloo();
                    hulla.send("Ссылка для восстановления пароля прислана вам на почту", "default");
                }
            }).fail(function (data, textStatus, xhr) {
                console.log(data, textStatus);
                $('.error-recovery-password').css('display', 'block');
        });
    }
});