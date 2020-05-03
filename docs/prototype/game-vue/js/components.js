Vue.component('card-player', {
    props: {
        player: Object
    },
    template: `
        <div class="card w3-card w3-round-large w3-white w3-hover-shadow w3-center">
            <p><strong>{{player.name}}</strong></p>
            <!-- Status gracza -->
            <template v-if="player.state == 'ready'">
                <p>Gotowy</p>
                <p><i class="icon-ok w3-text-green w3-xxxlarge"></i></p>
            </template>
            <template v-if="player.state == 'choosing'">
                <p>Wybiera..</p>
                <p><i class="icon-spin w3-xxxlarge w3-spin"></i></p>
            </template>
            <template v-if="player.state == 'master'">
                <p>Mistrz Kart</p>
            <p><i class="icon-eye w3-xxxlarge"></i></p>
            </template>
        </div>
    `
});
