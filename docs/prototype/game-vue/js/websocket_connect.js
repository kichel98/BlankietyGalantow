function connect() {
    parts = document.location.href.split('/')
    game_id = parseInt(parts[parts.length - 1])
    console.log(game_id)
        // game_id = 1
    socket = new WebSocket("ws://localhost:8000/connect/" + game_id);
    console.log("XDDD")
    return socket
}