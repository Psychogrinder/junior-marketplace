$(document).ready(function () {
    if ($('main .edit-profile').length > 0) {
        var consumer;
        var addr = window.location + '';
        addr = addr.split('/');
        var consumer_id = addr[addr.length - 2];
        $.ajax({
            url: "/api/v1/users/" + consumer_id,
            success: function (consumer_data) {
                console.log(consumer_data);
            }
        });
    }
});