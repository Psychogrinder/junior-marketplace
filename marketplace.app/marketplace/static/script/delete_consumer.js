function deleteConsumer() {
    var consumer_id = localStorage.getItem("globalUserId");
    $.ajax({
        url: '/api/v1/consumers/' + consumer_id,
        type: 'DELETE',
        success: function (result) {
            $('#agreeDeleteProfile').removeClass('show');
            $('#agreeDeleteProfile').css("display", "none");
            $('.modal-backdrop').css("display", "none");
            localStorage.setItem("globalUserId", null);
            localStorage.setItem("globalUserEntity", null);
            location.replace(window.location.origin);
        }
    });
}

$("#deleteConsumerBtn").click( function () {
    deleteConsumer()
});