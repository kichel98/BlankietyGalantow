let socket = connect();

const app = new Vue({
    el: '#game',
    methods: {
        selectCard: function(card) {
            if(this.me.state === "choosing") {
                if(card.selected) {
                    // Deselect the card
                    this.selectedCards.splice(this.selectedCards.indexOf(card),1);
                }
                else {
                    // Add card to the list of selected
                    this.selectedCards.push(card);
                }
                card.selected = !card.selected;
            }
        },
        confirmSelectedCards: function(player) {
            if(player.state === "choosing" && this.selectedCards.length===this.numberOfCardsToSelect && player.me) {
                player.state = "ready";
                // Making websocket message
                const data = {
                    type: "CARD_SELECT",
                    cards: this.selectedCards
                };
                
                // Send selected cards via websocket.
                socket.send(JSON.stringify(data));
            }
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
        }
    },
    computed: {
        me: function() {
            return this.players.filter((player)=>player.me)[0];
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
        players: [],
        myCards: [
            { id: 21, text: "Śmieszny tekst 1" },
            { id: 22, text: "Śmieszny tekst 2" },
            { id: 23, text: "Śmieszny tekst 3" },
            { id: 24, text: "Śmieszny tekst 4" },
            { id: 25, text: "Śmieszny tekst 5" },
            { id: 26, text: "Śmieszny tekst 6" },
            { id: 27, text: "Śmieszny tekst 7" },
            { id: 28, text: "Śmieszny tekst 8" },
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
        numberOfCardsToSelect: 3,
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
    if(data.type === "PLAYERS") {
        app.players = data.players
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
