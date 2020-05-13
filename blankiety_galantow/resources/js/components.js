Vue.component('room-item', {
    props: {
        room: Object
    },
    template: `
        <li>
            <div class="room-item hvr-icon-grow hvr-radial-out">
                <i class="icon-group room-icon w3-hide-small"></i>
                <div class="room">
                    <span class="w3-large">{{room.name}}</span><br>
                    <span>Gracze: {{room.players}}/{{room.maxPlayers}}</span>
                </div>
                <div class="room-status">
                    <i v-if="room.open && room.players < room.maxPlayers" class="hvr-icon icon-lock-open open"></i>
                    <i v-else-if="!room.open" class="hvr-icon icon-lock-closed closed"></i>
                    <i v-else="!room.open" class="hvr-icon icon-lock-closed-alt full"></i>
                </div>
            </div>
        </li>
    `
})
