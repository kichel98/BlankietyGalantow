
function connect() {
    const parts = document.location.href.split('/');
    const game_id = parts[parts.length - 1];
    const username = window.localStorage.getItem("username") || "Bezimienny";
    const port = window.location.port ? ":" + window.location.port : "";
    const host = window.location.hostname;
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const webSocketUrl = protocol + "//" + host + port + "/connect/" + game_id + "?username=" + username;
    return new WebSocket(webSocketUrl);
}
