$(document).ready(function () {
    if ((localStorage.getItem("globalUserId") > 0)) {
        let user_id = localStorage.getItem("globalUserId");
        $.get("/api/v1/chat/unread/" + user_id,
            function (numberOfMessages, status) {
                $('#numberOfUnreadMessagesBadge').html(numberOfMessages);
            });
    }
});