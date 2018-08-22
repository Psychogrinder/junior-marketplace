$("#authButton").click(function () {
    var email_authorisation = $("#emailAuthorisation").val();
    var password_authorisation = $("#passwordAuthorisation").val();

    if ( !email_authorisation ) {
        $("#emailAuthorisation").css("border-color", "#FF7851");
    }
    else if (!password_authorisation) {
         $("#passwordAuthorisation").css("border-color", "#FF7851");
    }
    else {
        $.post("/api/v1/login",
            {
                email: email_authorisation,
                password: password_authorisation,
            },
            function (status) {
                if(status) {
                    $('#singInUser').removeClass('show');
                    $('#singInUser').css("display", "none");
                    $('.modal-backdrop').css("display", "none");
                    location.reload();
                }
                else {
                    console.log('jopa');
                    $('#authUserAlert').css("display","block");
                }
            });

    }
});
