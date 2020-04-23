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
            this.chat.push({
                name: this.me.name,
                message: this.newMessage
            });

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
    data: {
        tableId: 20965,
        myId: 4,
        players: [
            {
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
            {id: 21, text: "Śmieszny tekst 1"},
            {id: 22, text: "Śmieszny tekst 2"},
            {id: 23, text: "Śmieszny tekst 3"},
            {id: 24, text: "Śmieszny tekst 4"},
            {id: 25, text: "Śmieszny tekst 5"},
            {id: 26, text: "Śmieszny tekst 6"},
            {id: 27, text: "Śmieszny tekst 7"},
            {id: 28, text: "Śmieszny tekst 8"},
        ],
        chat: [
            {name: "Gra", message: "Gracz Zuza dostaje punkt.", log: true},
            {name: "Gra", message: "Gracz Tomek zostaje mistrzem kart.", log: true},
            {name: "Michał", message: "Kurcze nic mi nie pasuje :("},
            {name: "Ala", message: "Oo to będzie mocne!"},
            {name: "Gra", message: "Gracz Zuza dostaje punkt.", log: true},
            {name: "Zuza", message: "Chyba jednak nie było xD"},
        ],
        newMessage: '',
        showPlayers: false,
        showChat: true,
        showSettings: false
    }
});