let socket = connect();

var game = new Vue({
    el: '#game',
    methods: {
        getPlayerById: function(id) {
            for (var p of this.players) {
                if (p.id === id)
                    return p;
            }
            return undefined;
        },
        sendMessage: function(event) {
            // Nie wysyłaj pustej wiadomości.
            if (this.newMessage === "")
                return;

            // Wysyłanie wiadomości...
            // this.chat.push({
            //     name: this.me.name,
            //     message: this.newMessage
            // });

            data = {
                type: "CHAT_MESSAGE",
                message: this.newMessage
            };

            // Testowe wysyłanie na websocket
            socket.send(JSON.stringify(data));

            this.newMessage = ''; // Po wysłaniu wiadomości wyczyść input.
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
                var element = document.getElementById("chat-content");
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
                state: "choosing",
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
        showSettings: false
    }
});


// Receive message from websocket
socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
	// TODO: check if data-type is CHAT_MESSAGE
    game.chat.push({
		log: data.log,
        name: data.user,
        message: data.message
    });
};
