const app = new Vue({
    el: '#container',
    methods: {
        connect: function(id) {
            window.location.pathname = "game/" + id;
        }
    },
    watch: {
        username: function(newName) {
            window.localStorage.setItem("username", this.username);
        }
    },
    /* Some mockup data */
    data: {
        username: window.localStorage.getItem("username") || "Bober",
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