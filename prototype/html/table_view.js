function showTable() {
    var commonView = document.getElementsByClassName("item_order");
    var tableView = document.getElementsByClassName("table_container");
    // var commonButton = document.getElementsById("common_mode");
    // var tableButton = document.getElementsById("table_mode");

    for (var i = 0; i < commonView.length; i++){
        commonView[i].classList.add("hidden");
    }

    for (var i = 0; i < tableView.length; i++){
        tableView[i].classList.remove("hidden");
    }
}

function showCommon() {
    var commonView = document.getElementsByClassName("item_order");
    var tableView = document.getElementsByClassName("table_container");
    // var commonButton = document.getElementsById("common_mode");
    // var tableButton = document.getElementsById("table_mode");

    for (var i = 0; i < tableView.length; i++){
        tableView[i].classList.add("hidden");
    }

    for (var i = 0; i < commonView.length; i++){
        commonView[i].classList.remove("hidden");
    }
}
