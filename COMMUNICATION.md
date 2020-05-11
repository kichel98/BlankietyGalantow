# Zasady komunikacji przez WebSockety


Komunikacja klient - serwer, po dołączeniu gracza do stołu, będzie się odbywać za pośrednictwem WebSocketów. Przez WebSockety przesyłane będą komunikaty w formacie JSON zserializowanym do string-a.

__Oznaczenia__

&#x1F4D8; Komunikaty bazowe (Potrzebne do podstawowej rozgrywki)

&#x1F4D7; Zmieniony komunikat bazowy, potrzebny do któregoś z dodatkowych wariantów gry

&#x1F4D9; Dodatkowy komunikat, potrzebny do któregoś z dodatkowych wariantów gry

## Komunikaty wysyłane przez klienta

### &#x1F4D8; Wybranie karty

```elixir
{
  type: "CARD_SELECT",
  tableId: int,
  message: {
    playerId: int,
    cardIds: {
      first: int,
      second: int,
      third: int,
      ...
    }
  }
}
```

### &#x1F4D8; Wybranie wygrywającej karty

```elixir
{
  type: "CHOOSE_WINNING_CARD",
  tableId: int,
  message: {
    playerId: int,
    cardId: int
  }
}
```

### &#x1F4D8; Wysłanie wiadomości na czacie

```elixir
{
  type: "CHAT_MESSAGE",
  tableId: int,
  message: {
    playerId: int,
    message: string
  }
}
```

### &#x1F4D8; Opuszczenie stołu

```elixir
{
  type: "LEAVE_TABLE",
  tableId: int,
  message: {
    playerId: int,
  }
}
```

## Wiadomości wysyłane przez serwer

### &#x1F4D8; Lista kart na ręce gracza

```elixir
{
  type: "PLAYER_HAND",
  tableId: int,
  message: {
    playerId: int,
    hand: [
      8xCard object {cardId:int , cardText: string}
    ]
  }
}
```

### &#x1F4D8; Wylosowana czarna karta

```elixir
{
  type: "BLACK_CARD",
  tableId: int,
  message: {
    cardId: int,
    cardText: string,
    whiteCardsNumber: int
  }
}
```

### &#x1F4D8; Wiadomość na czacie

```elixir
{
  type: "CHAT_MESSAGE",
  tableId: int,
  message: {
    playerId: int,
    playerName: string,
    message: string
  }
}
```

### &#x1F4D8; Przyznanie punktu zwycięstwa

```elixir
{
  type: "WIN_POINT",
  tableId: int,
  message: {
    playerId: int,
    playerName: string,
  }
}
```

### &#x1F4D8; Komunikat o kicku

```elixir
{
  type: "PLAYER_KICKED",
  tableId: int,
  message: {
    playerId: int,
    playerName: string,
  }
}
```
