# Zasady prowadzenia projektu

## Konwencja nazewnictwa
Stosujemy standardowe konwencje notyczące języków Python oraz JavaScript. Poniżej w tabeli jest wymienionych kilka przykładów.

| Struktura | Python | JavaScript |
| ----------| ------ | ---------- |
| zmienna | `some_var` | `someVar` |
| funkcja | `some_function()` | `someFunction()` |
| klasa   | `SomeClass` | `SomeClass` |

## Język polski i angielski
Jednoznacznie określamy kiedy stosujemy język angielski, a kiedy polski.

| Język | Kontekst |
| ----- | -------- |
| Angielski | Kod źródłowy, nazwy zmiennych, klas itd. |
| Angielski | Komentarze w kodzie źródłowym |
| Angielski | Nazwy katalogów w projekcie (wyjątek: dokumentacja) |
| Angielski | Nazwy branchy |
| Angielski | Nazwy commitów |
| Polski | Dokumentacja projektu |
| Polski | Issues na GitHubie |
| Polski | Ogólna komunikacja w tym repozytorium |

**Zachowujemy zdrowy rozsądek**. Nie spolszczamy na siłę słów powszechnie znanych i używanych: *branch*, *review*, *deadline*, *task*, *bug*, *endpoint*, *timeout* itd.

## Podział pracy na branche
Ustalamy konwencję *branch-per-feature*, tzn. tworzymy nowego brancha, gdy chcemy:
* Dodać nową funkcjonalność
* Dodać hotfixa
* Naprawić buga

Celem tworzenia branchy jest możliwość przejrzenia i skomentowania zmian przez innych członków zespołu na GitHubie nim zostaną one zmerge'owane do projektu. Daje to możliwość przetestowania zmian przed wdrożeniem.

Zmiany do swoich własnych branchy commitujemy bez obaw. Natomiast chcąc dodać funkcjonalność do brancha `dev` lub `master` powinno się najpierw utworzyć *Github Merge Request* i poczekać aż ktoś zrobi review zmian.

Usuwamy nieużywane branche, na których praca została zakończona.

Po raz kolejny zachowujemy zdrowy rozsądek. Jeśli zmiany są błahe i/lub pilne, to się nie powstrzymujemy przed ich dodaniem. Infrastruktura Gita i GitHuba ma służyć nam, a nie my jej (jakby powiedział pewien znany wieszcz).

## Nazewnictwo branchy
| Nazwa | Opis |
| ----- | ---- |
| `master` | Branch główny z działającą aplikacją |
| `docs` | Rozwijanie dokumentacji projektu |
| `dev` | Branch na aktualnie rozwijane funkcjonalności |
| `feat/some-name` | Branch na jakąś konkretną funkcjonalność |
| `hotfix/some-name` | Hotfix jakiejś niedawno dodanej zmiany |
| `bugfix/some-name` | Naprawa błędu |
| `some-name` | Gdy nic nie pasuje |

## Nazewnictwo commitów
Opisujemy zmiany, które zaszły. Pamiętajmy, że w nazwie commita możemy zawrzeć referencję do jakiegoś issue, np. `Fixed #16. Increased player limit per channel.` (jest to ficzer GitHuba, nie gita).
