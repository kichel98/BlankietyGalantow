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
    const parts = document.location.href.split('/');
    const game_id = parseInt(parts[parts.length - 1]);
    const username = getCookie("username");
    return new WebSocket("ws://localhost:80/connect/" + game_id + "?username=" + username);
}
