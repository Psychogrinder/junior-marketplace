namespace = '/chat';
if (localStorage.getItem("globalUserId")) {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
}


