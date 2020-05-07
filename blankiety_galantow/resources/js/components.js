Vue.component('server-item', {
    props: {
        server: Object
    },
    template: `
        <li>
            <a v-bind:href="'../game/index.html?id=' + server.id">
                <div class="server-item hvr-icon-grow hvr-radial-out">
                    <i class="icon-group server-icon w3-hide-small"></i>
                    <div class="server-info">
                        <span class="w3-large">{{server.name}}</span><br>
                        <span>Gracze: {{server.players}}/{{server.maxPlayers}}</span>
                    </div>
                    <div class="server-status">
                        <i v-if="server.open && server.players < server.maxPlayers" class="hvr-icon icon-lock-open open"></i>
                        <i v-else-if="!server.open" class="hvr-icon icon-lock-closed closed"></i>
                        <i v-else="!server.open" class="hvr-icon icon-lock-closed-alt full"></i>
                    </div>
                </div>
            </a>
        </li>
    `
})
