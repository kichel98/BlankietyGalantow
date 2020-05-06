function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

var app = new Vue({
    el: '#container',
    // I dont know react and vue, so this is quiet random ;) [Bartek]
    methods: {
        connect: function(id) {
            console.log(id)
            setCookie("game_id", id, 0.2)
            window.location.pathname = "game/" + id;
            console.log("http://localhost:8000/game/" + id)
        }
    },
    watch: {
        username: function(newName) {
            console.log("Zmieniono nazwę gracza na: " + newName);
            console.log("Zapisywanie do Local Storage...");
        }
    },
    /* Some mockup data */
    data: {
        username: "Bober",
        servers: [{
                id: 1,
                name: "Alpha",
                players: 1,
                maxPlayers: 6,
                open: true
            },
            {
                id: 2,
                name: "Beta",
                players: 3,
                maxPlayers: 6,
                open: false
            },
            {
                id: 3,
                name: "Charlie",
                players: 6,
                maxPlayers: 6,
                open: true
            }
        ]
    }

});