var app = new Vue({
    el: '#container',
    watch: {
        username: function(newName) {
            console.log("Zmieniono nazwę gracza na: " + newName);
            console.log("Zapisywanie do Local Storage...");
        }
    },
    /* Some mockup data */
    data: {
        username: "Bober",
        servers: [
            {
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
