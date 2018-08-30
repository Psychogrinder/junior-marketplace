$(document).ready(function () {
    $("#authButton").click(function () {
        var email_authorisation = $("#emailAuthorisation").val();
        var password_authorisation = $("#passwordAuthorisation").val();

        if (!email_authorisation) {
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
                function (data, status) {
                    if (status) {
                        $('#singInUser').removeClass('show');
                        $('#singInUser').css("display", "none");
                        $('.modal-backdrop').css("display", "none");
                        var globalUserId = data.id;
                        localStorage.setItem("globalUserId", globalUserId);
                        var globalUserEntity = data.entity;
                        localStorage.setItem("globalUserEntity", globalUserEntity);
                        location.reload();
                    }
                    else {
                        $('#authUserAlert').css("display", "block");
                    }
                });

        }
    });
    $("#logoutButton").click(function () {
        $.ajax({
            url: '/api/v1/logout',
            success: function () {
                localStorage.setItem("globalUserId", null);
                location.replace(window.location.origin);
            }
        });
    });
});
