import {mixin} from "./components.js";

const app = new Vue({
    el: '#container',
    mixins: [mixin],
    data: {
        showCreateRoomModal: false,
        username: window.localStorage.getItem("username") || "Bober",
        rooms: [],
        refreshRoomsInterval: null
    },
    // instead of `created` lifecycle hook, we can use `mounted`, if needed
    created: function() {
        const refreshRoomsPeriod = 5000;
        this.fetchRooms();
        this.refreshRoomsInterval = setInterval(() => {
            this.fetchRooms()
        }, refreshRoomsPeriod)
    },
    beforeDestroy: function () {
        clearInterval(this.refreshRoomsInterval)
    },
    methods: {
        fetchRooms: function() {
            fetch("/api/rooms")
                .then(response => response.json())
                .then(data => {
                    this.rooms = data.rooms;
                })
        },
        createRoom: function() {
            const room_name = document.getElementById("room-name").value;
            const room_seats = document.getElementById("room-seats").value;
            if(room_seats > 1){
                fetch(`/api/create?name=${room_name}&seats=${room_seats}`)
                .then(response => response.json())
                .then(data => {
                    this.connect(data.room_id)
                })
                this.showCreateRoomModal = false;
            } 
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
