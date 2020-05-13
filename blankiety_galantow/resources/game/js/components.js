Vue.component('card-player', {
    props: {
        player: Object
    },
    template: `
        <div class="card player w3-card w3-round-large w3-hover-shadow w3-center">
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
            <template v-if="player.state == 'selecting'">
                <p>Wybierz karty</p>
            <p><i class="icon-docs w3-xxxlarge"></i></p>
            </template>
        </div>
    `
});

// Vue.component("player-stack",{
//     props: {
//         playercards: Array,
//         revealedcards: Array
//     },
//     template: `
//         <div class="playerStack" 
//         v-bind:style="{ 'margin-left': playercards.length*30 + 'px'}">

//             <div v-for="card in playercards" v-bind:key="card.id">
//                 <div class="playerCard w3-card w3-round-large w3-hover-shadow w3-center w3-white" 
//                     v-bind:style="{ left: '-' + (playercards.length-playercards.indexOf(card))*30 + 'px',
//                                 top: '-' + (playercards.length-playercards.indexOf(card))*20 + 'px' }">
//                     <div v-if="revealedcards.indexOf(card)>0">
//                         {{card.text}}
//                     </div>
//                     <div class="order-bubble w3-round-xxlarge">
//                         {{playercards.indexOf(card)+1}}
//                     </div>
//                 </div>
//             </div>
//         </div>
//     `
// })
