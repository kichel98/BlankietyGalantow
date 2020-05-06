function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function connect() {
    game_id = getCookie("game_id")
    console.log(game_id)
        // game_id = 1
    socket = new WebSocket("ws://localhost:8000/connect/" + game_id);
    console.log("XDDD")
    return socket
}