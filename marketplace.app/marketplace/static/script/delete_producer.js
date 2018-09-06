

function deleteProducer() {
    producer_id = localStorage.getItem("globalUserId");
    $.ajax({
        url: '/api/v1/producers/' + producer_id,
        type: 'DELETE',
        success: function (result) {
            $('#deleteProfileProducer').removeClass('show');
            $('#deleteProfileProducer').css("display", "none");
            $('.modal-backdrop').css("display", "none");
            localStorage.setItem("globalUserId", null);
            localStorage.setItem("globalUserEntity", null);
            location.replace(window.location.origin);
        }
    });
}

$("#deleteProducerBtn").click( function () {
    deleteProducer()
});