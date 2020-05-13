function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

var app = new Vue({
    el: '#container',
    data: {
        username: "Bober",
        rooms: []
    },
    // instead of `created` lifecycle hook, we can use `mounted`, if needed
    created: function() {
      this.fetchRooms()
    },
    // I dont know react and vue, so this is quiet random ;) [Bartek]
    methods: {
        fetchRooms: function() {
            fetch("/api/rooms")
                .then(response => response.json())
                .then(data => {
                    this.rooms = data.rooms;
                })
        },
        connect: function(id) {
            setCookie("username", this.username, 1)
            window.location.pathname = "game/" + id;
        }
    },
    watch: {
        username: function(newName) {
            console.log("Zmieniono nazwę gracza na: " + newName);
            console.log("Zapisywanie do Local Storage...");
        }
    }
});