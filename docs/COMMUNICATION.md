# Zasady komunikacji przez WebSockety


Komunikacja klient - serwer, po dołączeniu gracza do stołu, będzie się odbywać za pośrednictwem WebSocketów. Przez WebSockety przesyłane będą komunikaty w formacie JSON zserializowanym do string-a.

__Oznaczenia__

&#x1F4D8; Komunikaty bazowe (Potrzebne do podstawowej rozgrywki)

&#x1F4D7; Zmieniony komunikat bazowy, potrzebny do któregoś z dodatkowych wariantów gry

&#x1F4D9; Dodatkowy komunikat, potrzebny do któregoś z dodatkowych wariantów gry

## Komunikaty wysyłane przez klienta

### &#x1F4D8; Wybranie karty

```js
{
  type: "CARD_SELECT",
  cards: [Int, ...]
}
```

### &#x1F4D8; Wybranie wygrywającej karty

```js
{
  type: "CHOOSE_WINNING_CARD",
  card: Int
}
```

### &#x1F4D8; Wysłanie wiadomości na czacie

```js
{
  type: "CHAT_MESSAGE",
  message: String
}
```

### &#x1F4D8; Zmiana ustawień

```js
{
  type: "SETTINGS_CHANGE",
  option: String,
  value: String
}
```

## Wiadomości wysyłane przez serwer

### &#x1F4D8; Lista kart na ręce gracza

```js
{
  type: "PLAYER_HAND",
  cards: [
    {
      id: Int,
      text: String
    }, 
    ...
  ]
}
```

### &#x1F4D8; Nowa karta
```js
{
  type: "NEW_CARD",
  card: {
    id: Int,
    text: String
  }
}
```

### &#x1F4D8; Wylosowana czarna karta

```js
{
  type: "BLACK_CARD",
  card: {
    id: Int,
    text: String
  }
}
```

### &#x1F4D8; Odświeżenie statusów graczy
```js
{
  type: "PLAYERS_STATE",
  states: [
    {
      playerId: Int,
      state: "ready" | "choosing" | "master"
    }
  ]
}
```

### &#x1F4D8; Odsłonięcie kart na stole
```js
{
  type: "CARD_REVEAL",
  cards: [
    {
      id: Int,
      text: String
    }
  ]
}
```

### &#x1F4D8; Wiadomość na czacie

```js
{
  type: "CHAT_MESSAGE",
  message: {
    log: Boolean,
    name: String,
    text: String
  }
}
```

### &#x1F4D8; Odświeżenie listy graczy

```js
{
  type: "PLAYER_LIST",
  players: [
    {
      id: Int,
      name: String,
      points: Int
    }
  ]
}
```

### &#x1F4D8; Odświeżenie ustawień pokoju

```js
{
  type: "SETTINGS",
  options: {
    "option-name": "value",
    "option-name": "value",
    ...
  }
  
}
```

