
function connect() {
    const parts = document.location.href.split('/');
    const game_id = parts[parts.length - 1];
    const username = window.localStorage.getItem("username") || "Bezimienny";
    return new WebSocket("ws://localhost:80/connect/" + game_id + "?username=" + username);
}
