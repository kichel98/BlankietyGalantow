Vue.component('card-player', {
    props: {
        player: Object
    },
    template: `
        <div class="card w3-card w3-round-large w3-hover-shadow w3-center w3-white">
            <p><strong>{{player.name}}</strong></p>
            <!-- Status gracza -->
            <template v-if="player.state == 'ready'">
                <p>Gotowy</p>
                <p><i class="icon-ok w3-text-green w3-xxxlarge"></i></p>
            </template>
            <template v-if="player.state == 'master'">
                <p>Mistrz Kart</p>
                <p><i class="icon-eye w3-xxxlarge"></i></p>
            </template>
            <template v-if="player.state == 'choosing'">
                <p>Wybiera..</p>
                <p><i class="icon-spin w3-xxxlarge w3-spin"></i></p>
            </template>
        </div>
    `
});

Vue.component('card-player-me', {
    props: {
        player: Object,
        readyToSubmit: Boolean
    },
    template: `
        <div class="card w3-card w3-round-large w3-hover-shadow w3-center"
             v-bind:class="{
                'select-animation': readyToSubmit,
                'faded': player.state == 'choosing' && !readyToSubmit
                }">
            <p><strong>{{player.name}}</strong></p>
            <!-- Status gracza -->
            <template v-if="player.state == 'ready'">
                <p>Gotowy</p>
                <p><i class="icon-ok w3-text-green w3-xxxlarge"></i></p>
            </template>
            <template v-if="player.state == 'master'">
                <p>Mistrz Kart</p>
            <p><i class="icon-eye w3-xxxlarge"></i></p>
            </template>
            <template v-if="player.state == 'choosing'">
                <p>Wybierz karty</p>
            <p><i class="icon-docs w3-xxxlarge"></i></p>
            </template>
        </div>
    `
});

Vue.component('card-stack', {
    props: {
        stack: Object,
    },
    template: `
        <div class="player-stack" 
            v-bind:style="{ 'margin-left': stack.cards.length*10 + 'px' }">

            <div v-for="(card, order) in stack.cards" 
                 v-bind:key="card.id"
                 class="player-card w3-card w3-round-large w3-hover-shadow w3-center w3-white" 
                 v-bind:class="{'on-top': stack.revealed && order == stack.currentCard}"
                 v-bind:style="{ 
                    left: '-' + (stack.cards.indexOf(card))*10 + 'px',
                    top: '-' + (stack.cards.indexOf(card))*10 + 'px' 
                 }">
                 
                <div v-if="stack.revealed">
                    {{card.text}}
                </div>  
                
                <div v-if="order == stack.currentCard && stack.revealed" 
                    class="order-bubble w3-round-xxlarge">
                    {{order + 1}}
                </div>
                
            </div>
        </div>   
    `
});

Vue.component('loader', {
    template: `
        <div class="w3-twothird">
            <div class="w3-panel w3-pale-yellow w3-leftbar w3-border-yellow w3-center">
                <p>Oczekiwanie na graczy</p>
            </div>
            <div class="loader">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
`})