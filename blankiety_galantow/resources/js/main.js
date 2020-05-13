const app = new Vue({
    el: '#container',
    data: {
        username: window.localStorage.getItem("username") || "Bober",
        rooms: []
    },
    // instead of `created` lifecycle hook, we can use `mounted`, if needed
    created: function() {
      this.fetchRooms()
    },
    methods: {
        fetchRooms: function() {
            fetch("/api/rooms")
                .then(response => response.json())
                .then(data => {
                    this.rooms = data.rooms;
                })
        },
        connect: function(id) {
            window.location.pathname = "game/" + id;
        }
    },
    watch: {
        username: function(newName) {
            window.localStorage.setItem("username", newName);
        }
    }
});
