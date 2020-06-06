let socket = connect();

const app = new Vue({
    el: '#game',
    methods: {
        selectCard: function(card) {
            if(this.me.state === "choosing") {
                if(this.customTextIsSet && this.customCardsUsed < this.settings.customCards) {
                    card.text = this.customText;
                    this.customText = "";
                    this.customCardsUsed++;
                    const data = {
                        type: "CUSTOM_CARD",
                        card: card
                    };
                    
                    // Send selected cards via websocket.
                    socket.send(JSON.stringify(data));
                }
                else
                {
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
            if(this.selectingWinnerMode) {
                this.selectWinner(stack);
                return;
            }

            if (stack.revealed)
                stack.currentCard = (stack.currentCard + 1) % stack.cards.length;

            // You can't reveal the stack if you're not a card master
            if(this.me.state !== "master")
                return;

            // First click reveals the stack
            stack.revealed = true;

            let card_ids = [];
            for(const card of stack.cards){
                card_ids.push(card.id);
            }

            const data = {
                type: "CARDS_REVEAL",
                cards: card_ids
            };
            socket.send(JSON.stringify(data));
        },
        selectWinner: function(stack) {
            // Sending CHOOSE_WINNING_CARDS message to server
            const data = {
                type: "CHOOSE_WINNING_CARDS",
                cards: stack.cards
            };
            socket.send(JSON.stringify(data));
        },
        exit: function() {
            window.location.pathname = "/";
        },
        clearError: function() {
            this.errorMessage = "";
        },
        submitSettings: function() {
            if(this.newSettings.time <= 0){
                return
            }
            const data = {
                type: "SETTINGS",
                settings: this.newSettings
            };
            socket.send(JSON.stringify(data));
            this.showSettings = false  // close settings modal
        },
        pauseGame: function() {
            if(this.me.admin){
                this.paused = !this.paused;
                const data = {
                    type: "PAUSED",
                    paused: this.paused
                };
                socket.send(JSON.stringify(data)); 
            }
        },
        submitPassword: function() {
            const data = {
                type: "PASSWORD",
                password: this.inputPassword
            };
            socket.send(JSON.stringify(data));
            this.passwordRequired = false  // close password modal
        },
        cancelSettingsChanges: function() {
            this.newSettings = Object.assign({}, this.settings);
            this.showSettings = false;
        },
        updateTimer: function() {
            this.timer = this.settings.time;
        },
        changePasswordRequired: function(event) {
            if(this.settingsPasswordRequired){
                this.settings.password = "";
            }
            this.settingsPasswordRequired = !this.settingsPasswordRequired
        }
    },
    computed: {
        me: function() {
            return this.players.filter((player)=>player.me)[0];
        },
        master: function() {
            return this.players.filter((player)=>player.state == 'master')[0];
        },
        gameLoaded: function() {
            return this.players.length > 0;
        },
        gameReady: function() {
            return this.players.length >= 2;
        },
        customTextIsSet: function() {
            return this.customText.length > 0;
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
        },
        formatedTimer: function() {
            let minutes = Math.floor(this.timer/60);
            let seconds = this.timer%60;
            return `${minutes}`.padStart(2,'0') + ':' + `${seconds}`.padStart(2,'0')
        } ,
        finalCountdown: function() {
            return this.timer < 10 && this.timer > 0;
        },
        timerState: function() {
            if(this.paused){
                return "Gra wstrzymana"
            }
            else{
                return "Gra w trakcie"
            }
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
        },
    },
    data: {
        players: [],
        myCards: [],
        chat: [],
        newMessage: '',
        errorMessage: '',
        settings: {
            roomName: "",
            customCards: 5,
            open: true,
            time: 60,
            gameType: "default",
            password: "",
        },
        settingsPasswordRequired: false,
        passwordRequired: false,
        passwordLength: 3,
        inputPassword: "",
        newSettings: {},
        showPlayers: false,
        showChat: true,
        showSettings: false,
        selectedCards: [],
        numberOfCardsToSelect: 3,
        timer: 0,
        paused: true,

        customCardsUsed: 0,
        customText: "",
        // Card master variables
        playedCards: [],
        selectingWinnerMode: false,
    }
});

setInterval(()=>{
    if(app.timer > 0 && app.players.length > 1 && !app.paused){
        app.timer = app.timer - 1;
    }
}, 1000);

// Receive message from websocket
socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if(!data.type) {
        console.error("Received incorrect message:");
        console.error(data);
        return;
    }
    if(data.type === "PASSWORD"){
        app.passwordRequired = true;
    }
    if(data.type === "PAUSED"){
        app.paused = data.paused;
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
        app.selectingWinnerMode = false;
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
                cards: card.playerCards,
            })
        }
        app.updateTimer();
    }
    if(data.type === "SELECT_RANDOM_CARDS") {
        app.selectedCards = [];
        for(const card of data.cards){
            app.selectCard(app.myCards.filter((myCard) => myCard.id === card.id)[0])
        }
    }
    if(data.type === "TIMER") {
        app.timer = data.timer
    }
    if(data.type === "SETTINGS") {
        app.settings = data.settings;
        app.newSettings = Object.assign({}, data.settings);
    }
    if(data.type === "KICK") {
        app.errorMessage = data.message;
    }
    if(data.type === "ERROR") {
        app.errorMessage = data.message || data.error
    }
    if(data.type === "CARDS_REVEAL"){
        for(const stack of app.playedCards){
            for(const card of stack.cards){
                if(!data.cards.includes(card.id)){
                    break;
                }
                stack.revealed = true;
            }
        }
    }
    // TODO: add other types of messages
};

socket.onclose = () => {
    if (app.errorMessage === "")
        app.errorMessage = "Połączenie z serwerem zostało przerwane."
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
