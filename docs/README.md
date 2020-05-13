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
* Ilość graczy: 3 – ∞ (górny limit do ustalenia w trakcie tworzenia GUI)
* Warunki zwycięstwa: zdobycie przez gracza ustalonej wcześniej ilości punktów
  
* Opis elementów rozgrywki:
  * Karta biała – zawiera krótką, maksymalnie jednozdaniową odpowiedź na kartę czarną. Ich skończona ilość jest elementem zestawu kart.
  * Karta czarna – zawiera krótkie pytanie lub zdanie z jedną lub dwoma lukami do uzupełnienia. Także zawiera się w zestawie kart.
  * Zestaw kart – pakiet kart białych i czarnych, o zazwyczaj spójnej tematyce. Administrator serwera może wybrać z których zestawów będą losowane karty przed rozpoczęciem rozgrywki.
  
* Przebieg rozgrywki:
  
    *W poniższym opisie, karta biała może być utożsamiana z parą kart białych w przypadku, gdy zagrana jest karta czarna z dwoma lukami.*
  1. Każdy gracz otrzymuje 10 losowych kart białych.
  2. Jeden z graczy, wedle kolejności na liście graczy, zostaje mistrzem kart. Wyświetlona zostaje losowa czarna karta.
  3. Pozostali gracze wybierają jedną z białych kart dostępnych na swojej ręce. Ich celem jest jest takie dopasowanie karty białej do czarnej, aby mistrz kart uznał ją za najśmieszniejszą.
  4. Białe karty zostają odkryte w taki sposób, by ich właściciele pozostali anonimowi. Mistrz kart oddaje głos na jedną z białych kart.
  5. Gracz, którego karta zwyciężyła zostaje ujawniony, wygrywa rundę i otrzymuje punkt. 
  6. Ręka każdego z graczy zostaje uzupełniona o dodatkowe losowe karty białe tak, by każdy z graczy ponownie posiadał 10 kart.
  7. Jeżeli żaden z graczy nie uzyskał ilości punktów wymaganej do zwycięstwa, wróc do punktu 2.
   
* Opcjonalne mechaniki, możliwe do zaimplementowania i uruchomienia przed rozpoczęciem gry:
  * **Mydełko** – Gracz może otrzymać pustą białą kartę, którą uzupełnia przed zagraniem jej maksymalnie 50 znakami tekstu.
  * **Czarny Jacek** – Mistrz kart przed wylosowaniem karty czarnej, może otrzymać możliwość własnoręcznego wybrania treści karty, do maksymalnie 100 znaków tekstu.
  * **Hazardista** – Gracz może zastawić swój punkt zwycięstwa w zamian za możliwość zagrania dwóch kart, lub zestawów kart białych. Jeżeli wygra rundę otrzymuje 2 punkty. W przeciwnym wypadku traci 1 punkt.
  * **Reset** – Gracz po zakończeniu rundy może wydać jeden punkt zwycięstwa na odrzucenie dowolnej ilości białych kart z ręki i zastąpieniem ich nowymi, losowo dobranymi kartami.
  * **Martwy mistrz** – Rola mistrza kart zostaje usunięta z gry, zwycięska karta biała jest wybierana na zasadzie głosowania.
  * **Przetrwają najsilniejsi** - Rola mistrza także zostaje usunięta. W trakcie głosowania gracze głosują na najmniej śmieszną kartę do czasu gdy pozostanie tylko jedna, której właściciel wygrywa rundę.
  * **Gramy na poważnie** – Mistrz kart wybiera 3 najśmiesznejsze karty, których właściciele otrzymują kolejno 3, 2 i 1 punkt zwycięstwa.
  * **Potęga chaosu** – Do rozgrywki dołącza bot Losowy Marcin, który w każdej turze zagrywa losowe karty białe. Jeżeli Losowy Marcin wygra rundę, gracze okrywają się hańbą i muszą zastanowić się nad swoim życiem.
  * **Pan i władca** – Mistrz kart może odrzucić niesmieszną czarną kartę, która zostaje zastąpiona nową.
  

### Czat
W trakcie rozgrywki dostępny jest czat dla graczy. Wiadomości wysyłane są tylko w obrębie danej rozgrywki. **Historia czatu nie jest w żaden sposób zachowywana po stronie serwera.** Backend jedynie przekazuje wiadomości do konkretnych użytkowników i natychmiast je zapomina.

### Ustawienia serwera
Będąc administratorem serwera użytkownik ma możliwość w dowolnej chwili je zmienić. Informacja o zmianie ustawień zostanie ogłoszona wszystkim użytkownikom na czacie. Dostępne opcje obejmują m. in.:
* Otwarcie / Zamknięcie serwera.
* Wybór hasła dostępu do serwera.
* Ustalenie ilości punktów wymaganej do zwycięstwa.
* Wyrzucenie gracza z rozgrywki (kick).
* Wybór zestawów kart dostępnych w rozgrywce.
* Uruchomienie opcjonalnych modyfikatorów rozgrywki opisanych szerzej w sekcji **Mechanika rozgrywki**

### Funkcjonalności dodatkowe
* Możliwość włączenia opcji "zaraz wracam", która pomija za nas kolejki
* Administrator serwera jako jedyny może rozpocząc grę, zpauzować ją lub zakończyć w dowolnym momencie.


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
Strona ta jest również pobierana z backendu w formie statycznej (wszystko jest początkowo puste). Znajdujący się na tej stronie kod JavaScipt ma za zadanie nawiązać połączenie z backendem za pomocą technologii WebSockets. Informacje, które są potrzebne do nawiązania połączenia, to:
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
| `/api/rooms` | JSON z listą serwerów         |
| `/game/{id}`   | HTML z frontem gry            |
| POST `/game/`  | *Utworzenie serwera*          |

**Funkcjonalności części statycznej:**
* Wysyłanie statycznych zasobów HTML, CSS i JS.
* Udostępnianie API z listą serwerów (JSON).
* Udostępnianie API umożliwiające dodanie nowego serwera.

### Część dynamiczna
Serce gry, w którym obsługiwane są połączenia przez WebSockets z przeglądarkami. Zadaniem tej części backendu jest zarządzanie stanem każdej trwającej aktualnie gry.

**Do przemyślenia**\
Cały backend działa na jednym wątku i opiera się o asynchroniczność (tutaj film świetnie wyjaśniający co to jest asynchroniczność na przykładnie Node: https://youtu.be/jOupHNvDIq8). W naszej grze karcianej nie ma akcji, które koniecznie muszą być wykonywane równolegle... z jednym wyjątkiem, a jest nim licznik czasu do końca tury, który dla każdej gry działa niezależnie i bez przerwy. Należy się zastanowić, czy da się to zaimplementować asynchronicznie.\
**Rozwiązanie**\
Można uruchomić asynchronicznie opóźnione zdarzenie, które da się też anulować: [call later](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.call_later). Jak mamy pecha, to może dojść do kolizji z innymi asynchronicznymi zdarzeniami. W tym celu można się posłużyć [lockiem](https://docs.python.org/3/library/asyncio-sync.html#asyncio.Lock).

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
