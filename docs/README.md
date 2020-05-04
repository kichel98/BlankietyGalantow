# Specyfikacja projektu

W tym katalogu znajduje się cała dokumentacja wraz z prototypami koncepcyjnymi, które powstały w trakcie realizacji projektu *Blankiety Galantów*.

## O projekcie

Blankiety Galantów jest grą karcianą, która umożliwia prowadzenie rozgrywek przez Internet pomiędzy użytkownikami. Wszystko uruchamiane jest w przeglądarce.

## Aspekty techniczne

### Wykorzystywane technologie
**Frontend**
* HTML + CSS
* JavaScript
* WebSockets
* Vue.js

**Backend**
* Python
* FastAPI

### Narzędzia pomocnicze
* GitHub - repozytorium
* GitHub issues - tworzenie i przydział zadań do wykonania
* Github project board - zarządzanie postępem
* GitHub milestones - zarządzanie postępem

### Platformy docelowe
Gra będzie działać na każdej współczesnej przeglądarce Internetowej. Internet Explorer nie będzie oficjalnie wspierany przez ten projekt.

## Struktura projektu
Projekt dzieli się na dwie zasadnicze częśći: **Frontend** tworzony w technologiach webowych oraz **Backend** pisany w Pythonie. Obie części są hostowane w tym repozytorium i razem tworzą jedną, działającą aplikację. Dokładniejsze szczegóły oraz zadania realizowane przez każdą z warstw zostaną omówione niżej.

## Funkcjonalności
Aby zagrać w grę nie trzeba zakładać konta. Wystarczy wybrać serwer i do niego dołączyć. Każdy z graczy automatycznie ma przydzielony nick, który może jednak zmienić.

### Dołączanie do serwera
Użytkownik uruchamia aplikację pod adresem, np. https://blankiety-galantow.pl i jego oczom ukazuje się lista serwerów do wyboru. Użytkownik w tym momencie może zmienić swój nick oraz dołączyć do dowolnego *otwartego* serwera.

Alternatywnym sposobem na dołączenie do wybranego serwera jest przejście pod link udostępniony przez jednego z graczy, np. https://blankiety-galantow.pl/game/12345.

### Mechanika rozgrywki
*Opis krok po kroku wszystkich stanów rozgrywki po kolei. Najlepiej na jakimś przykładzie z 3 osobami.*

### Czat
W trakcie rozgrywki dostępny jest czat dla graczy. Wiadomości wysyłane są tylko w obrębie danej rozgrywki. **Historia czatu nie jest w żaden sposób zachowywana po stronie serwera.** Backend jedynie przekazuje wiadomości do konkretnych użytkowników i natychmiast je zapomina.

### Ustawienia serwera
Będąc administratorem serwera użytkownik ma możliwość w dowolnej chwili je zmienić. Informacja o zmianie ustawień zostanie ogłoszona wszystkim użytkownikom na czacie. Dostępne opcje obejmują m. in.:
* Otwarcie / Zamknięcie serwera
* Wyrzucenie gracza z rozgrywki (kick)
* Zmiana trybu gry (?)

### Funkcjonalności dodatkowe
* Karta specjalna "wpisz co chcesz"
* Możliwość włączenia opcji "zaraz wracam", która pomija za nas kolejki
* Możliwość wydania zdobytych punktów na umiejętności specjalne typu:
  * Wymień wybrane białe karty na ręce
  * Wymień nieśmieszną czarną kartę
  * Dodaj białą kartę do talii (każdy gracz może ją wyciągnąć)
  * Dodaj czarną kartę do tablii

## Frontend
W całości pisany w technologiach webowych interfejs składający sie ze statycznych plików HTML+CSS+JS opartych o Vue.js. Na cały interfejs składają się dwa niezależne od siebie widoki

### Widok listy serwerów
Strona jest pobierana z backendu bez listy serwerów. Dopiero załadowanie JavaScriptu umieszczonego w tym zasobie pozwoli asynchronicznie pobrać listę serwerów z REST API i załadować ją w odpowiednie miejsce w HTML (Vue.js).

**Funkcjonalności widoku:**
* Pobieranie serwerów z REST API.
* Wyświetlanie listy serwerów pobranych z REST API.
* Interfejs do zakładania nowego serwera.
* Pole do wpisania swojego nicku
* Możliwość dołączenia do wybranego serwera

Uwaga implementacyjna: początkowo możemy predefiniować pewną liczbę serwerów, a funkcjonalnością zakładania swojego serwera zostawić na koniec. Czyli w celach testu uruchamiamy np. 10 serwerów.

### Widok ekranu gry
Strona ta jest również pobierana z backendu w formie statycznej (wszystko jest początkowo puste). Znajdujący się na tej stronie kod JavaScipt ma za zadanie nawiązać połączenie z backendem za pomocą technologii WebScoekts. Informacje, które są potrzebne do nawiązania połączenia, to:
* Nick gracza, który się łączy (odczytany np. z Local Storage)
* ID serwera (odczytany np. z linka: '[...]/game/12345')

Przy dołączaniu może wystąpić błąd, który należy czytelnie wyświetlić użytkownikowi:
* Serwer jest zamnięty
* Serwer jest pełny
* Inny błąd

Po nawiązaniu połączenia gracz automatycznie dostaje karty i bierze udział w rozgrywce. Nowy gracz zobaczy na czacie tylko wiadomości wysłane od momentu jego dołączenia.

Widok gry powinien się orientować w jakim stanie aktualnie znajduje się gra i wyświetlać graczowi odpowiednie informacje, np. "jesteś mistrzem kart", "wybierz kartę", "poczekaj na innych".

Widok powinien zapewniać interfejs adekwatny do sytuacji, np. mistrz kart nie może wystawić karty, a zwykły gracz nie może "wybrać zwycieżcy". Kliknięcie w złą kartę nie powinno mieć efektu w interfejsie.

**Funkcjonalności widoku:**
* Nawiązanie połączenia poprzez WebSockets.
* Ekran zmiany ustawień serwera.
* Zmiana ustawień serwera.
* Wysyłanie wiadomości na czacie.
* Wybieranie i zatwierdzanie kart.
* Wyświetlanie informacji co ma robić ("wybierz kartę", "poczekaj na innych" itd.)
* Odbieranie wiadomości od serwera i reagowanie na nie (gra + czat).

## Backend
Cały serwer wraz z obsługą gry zostanie napisany w Pythonie z użyciem FastAPI. Framework zapewnia wszystkie potrzebne funkcjonalności:
* Wysyłanie statycznych zasobów po HTTP (style, skrypty itd.).
* Łatwe wysyłanie JSON'a pod wskazanym endpointem.
* Wsparcie dla WebSockets
* Asynchroniczność

Cały backend będzie jest podzielony na dwie części *statyczną* oraz *dynamiczną*, które realizują swoje własne, odrębne zadania.

### Część statyczna
Jest to po prostu serwer HTTP udostępniający zasoby pod wskazanymi endpointami:
| Endpoint       | Zasób                         |
|----------------|-------------------------------|
| `/`            | HTML z frontem listy serwerów |
| `/api/servers` | JSON z listą serwerów         |
| `/game/{id}`   | HTML z frontem gry            |
| POST `/game/`  | *Utworzenie serwera*          |

**Funkcjonalności części statycznej:**
* Wysyłanie statycznych zasobów HTML, CSS i JS.
* Udostępnianie API z listą serwerów (JSON).
* Udostępnianie API umożliwiające dodanie nowego serwera.

### Część dynamiczna
Serce gry, w którym obsługiwane są połączenia przez WebSockets z przeglądarkami. Zadaniem tej części backendu jest zarządzanie stanem każdej trwającej aktualnie gry.

**Do przemyślenia**\
Cały backend działa na jednym wątku i opiera się o asynchroniczność (tutaj film świetnie wyjaśniający co to jest asynchroniczność na przykładnie Node: https://youtu.be/jOupHNvDIq8). W naszej grze karcianej nie ma akcji, które koniecznie muszą być wykonywane równolegle... z jednym wyjątkiem, a jest nim licznik czasu do końca tury, który dla każdej gry działa niezależnie i bez przerwy. Należy się zastanowić, czy da się to zaimplementować asynchronicznie.

#### Funkcjonalności
Funkcjonalności części dynamicznej mogą zostać podzielone na *moduły*, co ułatwi nam podział pracy. Warto zwrócić uwagę, że moduły o których mowa *nie są niezależne od siebie*, a współpracują i razem tworzą rdzeń gry. Nadmierna hermetyzacja i uniezależnianie modułów od siebie poprzez zaimplementowanie wszystkiego jako `private` nie jest wskazane. Nie o to chodzi w tych *modułach*.

**Moduł zarządzania połączeniem**\
Fragment systemu, który sprawuje pieczę nad procesem podłączania gracza do serwera. Może również podjąć pewne działania po zerwaniu połączenia z graczem. Zadania:
* Otwieranie połączenia WebSocket z graczem.
* Tworzenie obiektu gracza.
* W miarę łagodne dodanie gracza do serwera.
* Reagowanie na zerwanie połączenia z graczem.

**Moduł zarządzania stanem gry**\
Kod serwera, który orientuje się na jakim etapie rozgrywki znajduje się dany serwer. Do zadań tego moduły należy m. in.:
* Rozdawanie graczom kart.
* Losowanie czarnej karty.
* Wybieranie kolejnego mistrza kart.
* Weryfikacja poprawności ruchu gracza.
* Naliczanie punktów.

**Moduł czatu**
* Przekazuje wiadomości w obrębie danego serwera.

**Moduł ustawień**
* Zmienia ustawienia danego serwera.
* Weryfikuje czy użytkownik ma uprawnienia do zmiany ustawień.


## Harmonogram i kamienie milowe
Dokładny podział projektu na kamienie milowe zostanie zrealizowany przy pomocy narzędzi GitHuba. Wymienianie tutaj terminów mija się z celem, bo oznaczałoby to konieczność aktualizowania tego dokumentu. Tak czy inaczej można wskazać bardzo ogólne etapy postępu prac:
* Interfejs aplikacji (oba widoki)
* Wysyłanie statycznych zasobów
* Nawiązywanie połączenia z graczami i zarządzanie nimi
* Zarządzanie stanem gry
* Dodatkowe funkcjonalności 

## Zobacz również
* [Diagramy UML](diagrams/README.md)
* [Prototypy interfejsu](prototype/)
