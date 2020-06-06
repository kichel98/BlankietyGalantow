export const mixin = {
    methods: {
        isRoomFull: function (room) {
            return room.players >= room.maxPlayers
        }
    }
};

Vue.component('room-item', {
    mixins: [mixin],
    props: {
        room: Object
    },
    template: `
        <li>
            <div :class="isRoomFull(room) 
                    ? 'room-item not-allowed'
                    : 'room-item hvr-icon-grow hvr-radial-out pointer'">
                <i class="icon-group room-icon w3-hide-small"></i>
                <div class="room-info">
                    <span class="w3-large">{{room.name}}</span><br>
                    <span>Gracze: {{room.players}}/{{room.maxPlayers}}</span>
                </div>
                <div class="room-status">
                    <i v-if="isRoomFull(room)" class="hvr-icon icon-lock-open full"></i>
                    <i v-else-if="room.password" class="hvr-icon icon-lock-closed closed"></i>
                    <i v-else-if="room.open" class="hvr-icon icon-lock-closed-alt open"></i>
                    <i v-else class="hvr-icon icon-lock-closed closed"></i>
                </div>
            </div>
        </li>
    `
})

Vue.component('room-create-button', {
    props: {
        room: Object
    },
    template: `
        <li>
            <div id="create-room-btn" class="room-item w3-bottombar w3-border-black hvr-icon-grow hvr-radial-out pointer">
                <i class="icon-group room-icon w3-hide-small"></i>
                <div class="room-info">
                    <span class="w3-large">Nowy pokój</span><br>
                </div>
                <div class="room-status">
                    <i class="hvr-icon icon-plus-circled add-room"></i>
                </div>
            </div>
        </li>
    `
})