let socket = connect();

const app = new Vue({
    el: '#game',
    methods: {
        selectCard: function(card){
            if(this.getPlayerById(this.myId).state === 'selecting')
            {
                if(card.selected){               
                    this.selectedCards.splice(this.selectedCards.indexOf(card),1);
                }
                else
                {
                    this.selectedCards.push(card);
                }
                card.selected = !card.selected;
            }
        },
        confirmSelectedCards: function(player){
            if(player.state === "selecting" && this.selectedCards.length===this.cardsNumber){
                player.state = "ready";
                this.cardsConfirmed = true;
                // Making websocket message
                const data = {
                    type: "CARD_SELECT",
                    cards: this.selectedCards
                };
                
                // Send selected cards via websocket.
                socket.send(JSON.stringify(data));
            }
        },
        getPlayerById: function(id) {
            for (let p of this.players) {
                if (p.id === id)
                    return p;
            }
            return undefined;
        },
        sendMessage: function() {
            // Don't send empty messages.
            if (this.newMessage === "")
                return;

            const data = {
                type: "CHAT_MESSAGE",
                message: this.newMessage
            };

            // Send chat message via websocket.
            socket.send(JSON.stringify(data));

            this.newMessage = ''; // Clear the input element.
        },
        selectStack: function(playerCards) {
            
            this.revealedCards = this.revealedCards.concat(playerCards.filter((item)=>this.revealedCards.indexOf(item)<0));
            console.log(this.revealedCards);
            this.winningCards = playerCards;
        }
    },
    computed: {
        me: function() {
            return this.getPlayerById(this.myId);
        }
    },
    watch: {
        chat: function() {
            // Nowa wiadomość. Trzeba scrollować boxa. (Dirty Solution!)
            // Ta funkcja się uruchamia zanim Vue.js zaktualizuje DOM z czatem
            // dlatego tymczasowo robię takie coś ;D
            setTimeout(() => {
                const element = document.getElementById("chat-content");
                element.scrollTop = element.scrollHeight + 9999;
            }, 500);
        }
    },
    /* Mockup data */
    data: {
        tableId: 20965,
        myId: 4,
        players: [{
                id: 1,
                name: "Tomek",
                score: 1,
                state: "ready",
                admin: true
            },
            {
                id: 2,
                name: "Ala",
                state: "master",
                score: 0
            },
            {
                id: 3,
                name: "Michał",
                state: "choosing",
                score: 1
            },
            {
                id: 4,
                name: "Zuza",
                state: "master",
                score: 2
            }
        ],
        myCards: [
            { id: 21, text: "Śmieszny tekst 1", selected: false },
            { id: 22, text: "Śmieszny tekst 2", selected: false },
            { id: 23, text: "Śmieszny tekst 3", selected: false },
            { id: 24, text: "Śmieszny tekst 4", selected: false },
            { id: 25, text: "Śmieszny tekst 5", selected: false },
            { id: 26, text: "Śmieszny tekst 6", selected: false },
            { id: 27, text: "Śmieszny tekst 7", selected: false },
            { id: 28, text: "Śmieszny tekst 8", selected: false },
        ],
        chat: [
            { name: "Gra", message: "Gracz Zuza dostaje punkt.", log: true },
            { name: "Gra", message: "Gracz Tomek zostaje mistrzem kart.", log: true },
            { name: "Michał", message: "Kurcze nic mi nie pasuje :(" },
            { name: "Ala", message: "Oo to będzie mocne!" },
            { name: "Gra", message: "Gracz Zuza dostaje punkt.", log: true },
            { name: "Zuza", message: "Chyba jednak nie było xD" },
        ],
        newMessage: '',
        showPlayers: false,
        showChat: true,
        showSettings: false,
        selectedCards: [],
        cardsNumber: 3,

        // Card master variables
        playedCards: [
            {
                playerCards: [
                    { id: 21, text: "Śmieszny tekst 1"},
                    { id: 22, text: "Śmieszny tekst 2"},
                    { id: 23, text: "Śmieszny tekst 3"}
                ]
            },
            {
                playerCards: [
                    { id: 24, text: "Śmieszny tekst 4"},
                    { id: 25, text: "Śmieszny tekst 5"},
                    { id: 26, text: "Śmieszny tekst 6"}
                ]
            },
            {
                playerCards: [
                    { id: 27, text: "Śmieszny tekst 7"},
                    { id: 28, text: "Śmieszny tekst 8"},
                    { id: 29, text: "Śmieszny tekst 9"}
                ]
            }
        ],
        revealedCards: [

        ],
        winningCards: [

        ]
    }
});


// Receive message from websocket
socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if(!data.type) {
        console.error("Received incorrect message:");
        console.error(data);
        return;
    }
    if(data.type === "CHAT_MESSAGE" && data.message) {
        addMessageToChat(data.message);
    }
    // TODO: add other types of messages
};


function addMessageToChat(message) {
    if(message.user && message.text) {
        app.chat.push({
            log: message.log,
            name: message.user,
            message: message.text
        });
    }
}
