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
        confirmSelectedCards: function() {
            if(this.readyToSubmit) {
                this.me.state = "ready";
                // Making websocket message
                const data = {
                    type: "CARDS_SELECT",
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
        },
        onStackClick: function(stack) {
            // You can't reveal the stack if you're not a card master
            if(this.me.state !== "master")
                return;

            if(this.selectingWinnerMode) {
                this.selectWinner(stack);
                return;
            }

            if (stack.revealed)
                stack.currentCard = (stack.currentCard + 1) % stack.cards.length;

            // First click reveals the stack
            stack.revealed = true;
            // TODO: instead of revealing the stack by hand and changing the current
            //  card we can send that info  to the server so it notifies other players
            //  and cards are changed for all players.
        },
        selectWinner: function(stack) {
            // Sending CHOOSE_WINNING_CARDS message to server
            const data = {
                type: "CHOOSE_WINNING_CARDS",
                cards: stack.cards
            };
            socket.send(JSON.stringify(data));

            // TODO: If winner is correct then server sends empty playedCards
            //  temporarily we do it by hand
            this.playedCards = [];
        },
        exit: function() {
            window.location.pathname = "/";
        },
        clearError: function() {
            this.errorMessage = "";
        },
        // Use this function to fill playerCards with mockup data. Usefull for testing reactivity of webpage 
        tempFill: function() {
            this.playedCards = [
                {
                    revealed: false,
                    currentCard: 0,
                    cards: [
                        {id: 21, text: "Śmieszny tekst 1"},
                        {id: 22, text: "Śmieszny tekst 2"},
                        {id: 23, text: "Śmieszny tekst 3"}
                    ]
                },
                {
                    revealed: false,
                    currentCard: 0,
                    cards: [
                        { id: 24, text: "Śmieszny tekst 4"},
                        { id: 25, text: "Śmieszny tekst 5"},
                        { id: 26, text: "Śmieszny tekst 6"}
                    ]
                },
                {
                    revealed: false,
                    currentCard: 0,
                    cards: [
                        { id: 27, text: "Śmieszny tekst 7"},
                        { id: 28, text: "Śmieszny tekst 8"},
                        { id: 29, text: "Śmieszny tekst 9"}
                    ]
                }
            ];
        }
    },
    computed: {
        me: function() {
            return this.players.filter((player)=>player.me)[0];
        },
        gameLoaded: function() {
            return this.players.length > 0;
        },
        gameReady: function() {
            return this.players.length >= 2;
        },
        readyToSubmit: function() {
            // Check if player is ready to submit his/her selected cards
            return this.me.state === "choosing" && this.selectedCards.length === this.numberOfCardsToSelect;
        },
        selectingStage: function() {
            // If no cards are played then it's selecting stage.
            return this.playedCards.length === 0;
        },
        readingStage: function() {
            // If some cards are played then it's reading stage.
            return this.playedCards.length > 0;
        },
        allStacksRevealed: function() {
            let stacksRevealed = this.playedCards.every( stack => stack.revealed );
            return this.readingStage && stacksRevealed;
        },
        topInfo: function() {
            if(this.selectingStage) {
                if(this.me.state === "master") {
                    return "Jesteś mistrzem kart, zaczekaj aż wszyscy wybiorą karty";
                }
                if(this.me.state === "choosing") {
                    return "Wybierz karty, które chcesz zagrać";
                }
                if(this.me.state === "ready") {
                    return "Zaczekaj aż wszyscy wybiorą karty";
                }
            }
            if(this.readingStage && this.me.state !== "master") {
                return "Mistrz kart wybiera zwycięzcę";
            }
            if(this.readingStage && this.me.state === "master") {
                if(this.selectingWinnerMode) {
                    return "Wybierz najzabawniejsze dopasowanie";
                }
                else {
                    return "Odsłoń karty nadesłane przez graczy";
                }
            }
        },
        errorOccured: function() {
            return Boolean(this.errorMessage);
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
    data: {
        tableId: 20965,
        players: [],
        myCards: [],
        chat: [],
        newMessage: '',
        errorMessage: '',
        showPlayers: false,
        showChat: true,
        showSettings: false,
        selectedCards: [],
        numberOfCardsToSelect: 3,

        // Card master variables
        playedCards: [],
        selectingWinnerMode: false,
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
    if(data.type === "PLAYER_HAND" && data.cards) {
        app.myCards = data.cards;
        app.selectedCards = []
    }
    if(data.type === "BLACK_CARD" && data.card) {
        app.blackCard = data.card;
        app.numberOfCardsToSelect = parseInt(data.card.gap_count);
        app.selectingWinnerMode = false
    }
    if(data.type === "PLAYERS") {
        app.players = data.players;
    }
    if(data.type === "PLAYED_CARDS") {
        app.playedCards = [];
        // Message is weirdly parsed from JSON, that is why cards from data are extracted that way
        for(const card of data.cards){
            app.playedCards.push({
                revealed: false,
                currentCard: 0,
                cards: card.playerCards
            })
        }
    }
    if(data.type === "KICK") {
        app.errorMessage = data.message;
    }
    if(data.type === "ERROR") {
        app.errorMessage = data.message || data.error
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
