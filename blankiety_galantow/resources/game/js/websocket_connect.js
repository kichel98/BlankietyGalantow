
function connect() {
    const gameId = document.location.pathname.split('/')[2]; // pathname: /game/{gameId}
    const username = window.localStorage.getItem("username") || "Bezimienny";
    const port = window.location.port ? ":" + window.location.port : "";
    const host = window.location.hostname;
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const webSocketUrl = protocol + "//" + host + port + "/connect/" + gameId + "?username=" + username;
    return new WebSocket(webSocketUrl);
}
